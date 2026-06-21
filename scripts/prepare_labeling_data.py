from pathlib import Path
import json

import pandas as pd

PLAYER_MAP = {
    "watch1": "player_1",
    "watch2": "player_2",
    "watch3": "player_3",
    "watch4": "player_4",
}


def prepare_labeling_data(
    root: Path = Path("./data"),
    base_url: str = "http://localhost:8000/data",
    overwrite: bool = False,
) -> None:
    for raw_file in root.rglob("heartbeat_raw.csv"):
        game_dir = raw_file.parent

        relative_parts = game_dir.relative_to(root).parts
        game_name = "-".join(relative_parts)

        converted_file = game_dir / "heartbeat_converted.csv"
        metadata_file = root / f"{game_name}.json"

        if not overwrite and converted_file.exists() and metadata_file.exists():
            print(f"skip: {game_name}")
            continue

        print(f"processing: {game_name}")

        # CSV変換
        df = pd.read_csv(raw_file)

        df["player"] = df["device_id"].map(PLAYER_MAP)

        wide = df.pivot_table(
            index="timestamp",
            columns="player",
            values="heartbeat",
            aggfunc="last",
        ).reset_index()

        for col in ["player_1", "player_2", "player_3", "player_4"]:
            if col not in wide.columns:
                wide[col] = pd.NA

        wide = wide[["timestamp", "player_1", "player_2", "player_3", "player_4"]]

        wide["timestamp"] = (wide["timestamp"] - wide["timestamp"].min()) / 1000.0

        wide.to_csv(converted_file, index=False)

        # URLは元のディレクトリ構造を維持
        relative_path = game_dir.relative_to(root).as_posix()

        metadata = {
            "video": f"{base_url}/{relative_path}/video.mp4",
            "timeseries": f"{base_url}/{relative_path}/heartbeat_converted.csv",
        }

        with open(metadata_file, "w", encoding="utf-8") as f:
            json.dump(metadata, f, ensure_ascii=False, indent=2)

        print(f"saved: {converted_file}")
        print(f"saved: {metadata_file}")


if __name__ == "__main__":
    prepare_labeling_data(overwrite=True)
