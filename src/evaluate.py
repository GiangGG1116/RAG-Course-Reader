from typing import List, Dict
import pandas as pd
from ragas import evaluate
from ragas.metrics import context_precision, context_recall, faithfulness, answer_relevancy
from src.generate import get_answer
from src.embed_index import load_index


# Đánh giá trên bộ câu hỏi có ground truth (csv: question, answer)


def evaluate_csv(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)
    records = []
    for _, row in df.iterrows():
        q = row["question"]; gt = row.get("answer", None)
        ans, ctx = get_answer(q)
        records.append({"question": q, "answer": ans, "contexts": [d.page_content for d in ctx], "ground_truth": gt})
    eval_df = pd.DataFrame(records)


    try:
        res = evaluate(
            eval_df.rename(columns={"ground_truth": "ground_truth"}),
            metrics=[context_precision, context_recall, faithfulness, answer_relevancy],
        )
        return res.to_pandas()
    except Exception:
        return eval_df