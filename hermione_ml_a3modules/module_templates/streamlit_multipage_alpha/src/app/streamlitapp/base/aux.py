import os
import pandas as pd
from st_aggrid import AgGrid, GridOptionsBuilder, DataReturnMode, GridUpdateMode
import datetime
import streamlit as st
import glob
import s3fs

fs = s3fs.S3FileSystem()


def files_select_ag_grid(add_current=False, mode="single"):

    file_list = [
        x.replace(".pickle", "") for x in list_dir("saved_sessions") if ".pickle" in x
    ]
    file_times = [
        # datetime.datetime.fromtimestamp(
        get_m_time(os.path.join("saved_sessions", f"{x}.pickle"))
        # )
        for x in file_list
    ]

    files_desc = []
    for f_name in file_list:
        desc_f_name = os.path.join("saved_sessions", f"{f_name}.txt")
        if file_exists(desc_f_name):
            files_desc.append(open_file(desc_f_name).read())
        else:
            files_desc.append("")

    if add_current:
        file_list = ["Análise Atual"] + file_list
        file_times = [""] + file_times
        files_desc = [""] + files_desc

    input_df = pd.DataFrame(
        list(zip(file_list, file_times, files_desc)),
        columns=["Nome", "Ùltima Modificação", "Descrição"],
    )

    gb = GridOptionsBuilder.from_dataframe(input_df)
    gb.configure_selection(mode, use_checkbox=True)
    gridOptions = gb.build()

    update_mode_value = GridUpdateMode.__members__["MODEL_CHANGED"]

    return AgGrid(
        input_df,
        gridOptions=gridOptions,
        update_mode=update_mode_value,
        height=200,
    )


def get_path(fpath, add_prefix=True):
    if add_prefix:
        if os.environ["APP_ENV"] == "production":
            return os.path.join(
                os.environ["BUCKET_PATH"],
                fpath,
            )
        else:
            return os.path.join(
                "/usr/src/app",
                fpath,
            )
    else:
        return fpath


def get_m_time(fpath, add_prefix=True):
    fpath = get_path(fpath, add_prefix)
    if os.environ["APP_ENV"] == "production":
        return fs.info(fpath)["LastModified"]
    else:
        return os.path.getmtime(fpath)


def file_exists(fpath, add_prefix=True):

    fpath = get_path(fpath, add_prefix)
    if os.environ["APP_ENV"] == "production":
        return fs.exists(fpath)
    else:
        return os.path.exists(fpath)


def list_dir(fpath, add_prefix=True):

    fpath = get_path(fpath, add_prefix)

    if os.environ["APP_ENV"] == "production":
        fpaths = fs.ls(fpath)
        return [os.path.relpath(x, fpath) for x in fpaths]
    else:
        return os.listdir(fpath)


def open_file(fpath, mode="r", add_prefix=True):

    fpath = get_path(fpath, add_prefix)

    if os.environ["APP_ENV"] == "production":
        return fs.open(fpath, mode=mode)
    else:
        return open(fpath, mode)


def fs_glob(fpath, add_prefix=True):

    fpath = get_path(fpath, add_prefix)

    if os.environ["APP_ENV"] == "production":
        return fs.glob(fpath)
    else:
        return glob.glob(fpath)


def get_file_content_as_string(path):
    with open_file(path) as f:
        return f.read()


def get_csv_as_df(path):
    return pd.read_csv(open_file(path))


def get_parquet_as_df(path):
    def pd_read_pattern(pattern):
        files = fs_glob(pattern)

        df = pd.DataFrame()
        for f in files:
            df = df.append(pd.read_parquet(open_file(f, "rb", add_prefix=False)))
        return df

    return pd_read_pattern(path)