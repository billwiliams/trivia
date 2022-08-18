

def paginate(request, selection, NUM_ITEMS_TO_PAGINATE):
    page = request.args.get("page", 1, type=int)
    start = (page - 1) * NUM_ITEMS_TO_PAGINATE
    end = start + NUM_ITEMS_TO_PAGINATE

    items = [item.format() for item in selection]
    paginated_items = items[start:end]

    return paginated_items
