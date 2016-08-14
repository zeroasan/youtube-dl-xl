DROP TABLE IF EXISTS video_info;
create table video_info (
    id          integer primary key autoincrement not null,
    url         text,
    uploader    text,
    author      text,
    downloadTime date,
    downloadPath text,
    isDownloaded  integer default 0,
    isUploaded    integer default 0, --not used
    isProcessing  integer default 0,
    description text
);