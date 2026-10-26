def paginate(query, page, page_size):
    """对 SQLAlchemy 查询对象进行分页，返回统一结构"""
    total = query.count()
    pages = -(-total // page_size) if total else 0  # 向上取整
    items = query.offset((page - 1) * page_size).limit(page_size).all()
    return {
        "total": total,
        "page": page,
        "pageSize": page_size,
        "pages": pages,
        "items": [item.to_dict() for item in items],
    }
