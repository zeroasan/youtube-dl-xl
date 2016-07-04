create table video_info (
    id          integer primary key autoincrement not null,
    url         text,
    uploader    text,
    author      text,
    isDownloaded  integer default 0,
    isUploaded    integer default 0,
    description text
);