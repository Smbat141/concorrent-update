from inbound_request.inbound_request import InboundRequest

permitted_params = ['param_1', 'param_2']
request_data = {'param_1': 'value_1', 'param_2': 'value_2'}

filter_permitted_params = ['filter_param_1', 'filter_param_2']
filter_request_data = {'filter_param_1': 'value_1'}


def test_inbound_request_permitted_params_not_valid(app):
    with app.test_request_context():
        # request is null inside InboundRequest
        inbound_request = InboundRequest()
        fetched_data = inbound_request.fetch_permitted_params(permitted_params)

    assert fetched_data['is_valid'] is False
    assert fetched_data['message'] == "following params are required ['param_1', 'param_2']"


def test_inbound_request_permitted_params_valid(app):
    with app.test_request_context() as req:
        inbound_request = InboundRequest()
        req.request.args = request_data

        fetched_data = inbound_request.fetch_permitted_params(permitted_params)

    assert fetched_data['is_valid'] is True
    assert fetched_data['params'] == request_data


def test_inbound_request_filter_permitted_params_not_valid(app):
    with app.test_request_context():
        inbound_request = InboundRequest()
        fetched_data = inbound_request.fetch_filter_params(filter_permitted_params)

    assert fetched_data['is_valid'] is False
    assert fetched_data['message'] == "following params are required ['filter_param_1', 'filter_param_2']"


def test_inbound_request_filter_permitted_params_valid(app):
    with app.test_request_context() as req:
        inbound_request = InboundRequest()
        req.request.args = filter_request_data

        fetched_data = inbound_request.fetch_filter_params(filter_permitted_params)

    assert fetched_data['is_valid'] is True
    assert fetched_data['filter_by'] == filter_request_data['filter_param_1']


def test_inbound_request_is_is_there_mismatch_when_false(app):
    with app.test_request_context():
        inbound_request = InboundRequest()
        is_false = inbound_request.is_there_mismatch({'param_1': None})

    assert is_false is False


def test_inbound_request_is_is_there_mismatch_when_true(app):
    with app.test_request_context():
        inbound_request = InboundRequest()
        is_true = inbound_request.is_there_mismatch({'param_1': 'value_1'})

    assert is_true is True
