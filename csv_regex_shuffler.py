import re
from datetime import datetime
from random import seed, randint
import pandas as pd

# enter the column name with which to apply the regex to
col_name = 'Image'
# enter path the csv file you want to shuffle
unshuffled_csv = r"data\new_dataset\combined\new_datasets_combined.csv"
# specify the regex that extracts the unique identifier from the path
unique_id_regex = r"(?<=objectNo-)([0-9]*)"


# specify the regex that checks if the unique identifier is in any other rows path
def pattern_match_regex(unique_id):
    return f"objectNo-{unique_id}-+[0-9|a-z]*-+[0-9|a-z]*-+[0-9]*"


def get_unique_id_from_path(path):
    unique_id = re.findall(unique_id_regex, path)[0]
    return unique_id


def main():
    df1 = pd.read_csv(unshuffled_csv)
    df2 = pd.DataFrame(
        columns=["Image", "X Offset", "Y Offset", "x_pix_offset", "y_pix_offset", "x_mag_bin", "y_mag_bin", "zoom"])
    max_row = len(df1.index)

    while max_row > 0:
        # randomly generate a number from 0 to maxRow
        rnd_idx = randint(0, max_row - 1)
        # get specified column value at that row index
        col_value = df1.iloc[rnd_idx][col_name]
        print(col_value)
        # apply regex to find the unique identifier in the name
        unique_id = get_unique_id_from_path(col_value)
        # group all rows that match the pattern of the regex into a dataframe.
        obj_group = df1[df1[col_name].str.contains(pattern_match_regex(unique_id))]
        # concat the groups dataframe to df2
        df2 = pd.concat([obj_group, df2])
        df2 = df2.reset_index(drop=True)
        # df1 = df1-df2 to remove the processed rows from df1
        df1 = df1.append(df2)
        df1 = pd.concat([df1, df2, df2]).drop_duplicates(keep=False)
        df1 = df1.reset_index(drop=True)
        # update max row
        max_row = len(df1.index)
    # replace the old file with the new, shuffled CSV dataframe
    df2.to_csv(unshuffled_csv, index=False)


if __name__ == '__main__':
    main()
