"""Product search endpoint module
"""
from api.product.v1.views import product_views
from flask import abort, jsonify, request
from models import storage
from models.product import Product
from models.subcategory import Subcategory


@product_views.route("/search/products", strict_slashes=False)
def search_for_products():
    """ Searches for products based on product description,
        brand, maximum price and minimum price
        Args: None
        Return: dictionary with a list of objects
                matching search criteria
    """
    from api.product.v1.views.products import modify_product_output
    filters = request.args
    if not filters:
        abort(400)
    search_query = filter.get('search_query').lower()
    products = storage.search(Product)
    search_results = []

    # Search product by search query
    for product in products:
        description = product.description.lower()
        name = product.name.lower()
        if search_query in description or search_query in name:
            search_results.append(modify_product_output(product))

    search_results = filter_products(filters, search_results)
    return jsonify(search_results)


@product_views.route("/search/<subcategory_id>/products", strict_slashes=False)
def search_for_products_by_category(subcategory_id):
    """ Searches for products based on product description,
        brand, maximum price and minimum price
        Args: None
        Return: dictionary with a list of objects
                matching search criteria
    """
    from api.product.v1.views.products import modify_product_output

    filters = request.args
    if not filters:
        abort(400)

    # Validate subcategory
    subcategory = storage.search(Subcategory, subcategory_id)
    if not subcategory:
        abort(404)

    # Search product by subcategory
    products = subcategory.products
    search_results = [modify_product_output(product) for product in products]

    # Filter search results
    search_results = filter_products(filters, search_results)
    return jsonify(search_results)


def filter_products(filters, search_results):
    """ Filters query results based on given filters
        Args:
            filters (dict/multidict): dictionary of filter parameters
            search_results (list): list of search results to filter
        Return: dictionary of such filter results
    """
    brand = filters.get('brand')
    max_price = filters.get('max')
    min_price = filters.get('min')
    if brand:
        search_results = [result for result in search_results
                          if brand == result.get('brand')]
    if min_price:
        search_results = [result for result in search_results
                          if result.get('price') >= min_price]
    if max_price:
        search_results = [result for result in search_results
                          if result.get('price') <= max_price]
    search_results = {"count": len(search_results), "products": search_results}
    return search_results
