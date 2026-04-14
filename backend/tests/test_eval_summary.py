from eval.run_eval import EvalResult, build_summary, compute_accuracy


def test_compute_accuracy_and_summary() -> None:
    results = [
        EvalResult(
            filename="linen-shirt.jpg",
            expected={
                "garment_type": "top",
                "style": "contemporary",
                "base_colour": "white",
            },
            predicted={
                "garment_type": "top",
                "style": "contemporary",
                "base_colour": "black",
            },
        )
    ]

    scores = compute_accuracy(results)
    summary = build_summary(results, scores)

    assert scores["garment_type"]["strict"] == 1.0
    assert scores["garment_type"]["semantic"] == 1.0
    assert scores["base_colour"]["strict"] == 0.0
    assert scores["base_colour"]["semantic"] == 0.0
    assert "linen-shirt.jpg" in summary
    assert "Per-Attribute Accuracy" in summary
    assert "Semantic Relaxed Accuracy" in summary
