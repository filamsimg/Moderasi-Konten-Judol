from typing import Iterable, List


def _chunk(items: List[str], size: int) -> Iterable[List[str]]:
    for i in range(0, len(items), size):
        yield items[i : i + size]


class ModelService:
    def __init__(self, model_path: str, device: str, max_length: int, batch_size: int):
        self.model_path = model_path
        self.device = device
        self.max_length = max_length
        self.batch_size = batch_size
        self._tokenizer = None
        self._model = None
        self._torch = None

    @property
    def loaded(self) -> bool:
        return self._model is not None

    def load(self) -> None:
        import torch
        from transformers import AutoModelForSequenceClassification, AutoTokenizer

        self._torch = torch
        if self.device.startswith("cuda") and not torch.cuda.is_available():
            self.device = "cpu"
        self._tokenizer = AutoTokenizer.from_pretrained(self.model_path)
        self._model = AutoModelForSequenceClassification.from_pretrained(self.model_path)
        self._model.to(self.device)
        self._model.eval()

    def predict_scores(self, texts: List[str]) -> List[float]:
        if not self.loaded:
            raise RuntimeError("Model is not loaded")
        if not texts:
            return []

        scores: List[float] = []
        for batch in _chunk(texts, max(1, self.batch_size)):
            inputs = self._tokenizer(
                batch,
                padding=True,
                truncation=True,
                max_length=self.max_length,
                return_tensors="pt",
            )
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with self._torch.no_grad():
                outputs = self._model(**inputs)
                logits = outputs.logits
                if logits.shape[-1] == 1:
                    probs = self._torch.sigmoid(logits).squeeze(-1)
                else:
                    probs = self._torch.softmax(logits, dim=-1)[:, 1]
                scores.extend(probs.detach().cpu().tolist())
        return scores
