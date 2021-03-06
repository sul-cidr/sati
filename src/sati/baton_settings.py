BATON = {
    "SITE_HEADER": "SATI :: Database&nbsp;Administration",
    "SITE_TITLE": "SATI :: Database Administration",
    "INDEX_TITLE": "Database Administration",
    "CONFIRM_UNSAVED_CHANGES": True,
    "SHOW_MULTIPART_UPLOADING": True,
    "ENABLE_IMAGES_PREVIEW": False,  # disabling, so as to reimplement
    "GRAVATAR_DEFAULT_IMG": "identicon",
    "CHANGELIST_FILTERS_IN_MODAL": False,
    "MENU_ALWAYS_COLLAPSED": False,
    "MENU_TITLE": "",
    "MENU": (
        {"type": "title", "label": "Test Items", "apps": ("items",)},
        {
            "type": "model",
            "label": "All Items",
            "name": "item",
            "icon": "fa fa-fw fa-file-invoice",
            "app": "items",
        },
        {
            "type": "free",
            "label": "Items Requiring Attention",
            "icon": "fa fa-fw fa-exclamation-circle",
            "url": "/admin/items/item/?requires_attention__exact=1",
        },
        {
            "type": "model",
            "label": "Tests",
            "name": "test",
            "icon": "fa fa-fw fa-list-ol",
            "app": "items",
        },
        {"type": "title", "label": "Website Config", "apps": ("users",)},
        {
            "type": "model",
            "label": "Users",
            "name": "user",
            "icon": "fa fa-fw fa-users",
            "app": "users",
        },
        {"type": "title", "label": "External Links"},
        {
            "type": "free",
            "label": "SATI Homepage",
            "icon": "fa fa-fw fa-home",
            "url": "/",
        },
        {
            "type": "free",
            "label": "SATI Team Drive",
            "icon": "fab fa-fw fa-google-drive",
            "url": "https://drive.google.com/drive/folders/0AFa5CSv6KYQSUk9PVA",
        },
        {
            "type": "free",
            "label": "SATI Issue Tracker",
            "icon": "fab fa-fw fa-github-square",
            "url": "https://github.com/sul-cidr/sati/issues/",
        },
    ),
}
