from dataclasses import dataclass
from pathlib import Path

BASE_DIR = Path(__file__).parent


@dataclass
class Config:
    goal: int = 2 * (3600 * 6)  # 12 hours a week
    min_time: int = (5 * 60)  # minimum time for plotting (5 minute)
    save_path = BASE_DIR / 'fig'  # path of preservation graphics
    min_percentage: int = 1  # the minimum percentage for calculations and plotting
    max_activities: int = 13  # maximum number of activities. Recommended value 13-15
    max_title_len: int = 12  # maximum length of the activity name
    colors_tuple: tuple = (
        'forestgreen', 'limegreen', 'green', 'lime', 'seagreen', 'mediumseagreen',
        'cornflowerblue', 'royalblue', 'midnightblue', 'navy', 'darkblue',
        'blueviolet', 'indigo', 'darkorchid', 'mediumorchid', 'violet', 'purple',
        'teal', 'aqua', 'deepskyblue', 'steelblue', 'dodgerblue'
    )  # The blue color has been reserved. Warning! It is not worth using for a unique color of activity.
    db_name: str = 'activityTracker'
    table_name: str = 'activities'



settings = Config()

__all__ = ('settings', 'BASE_DIR')
