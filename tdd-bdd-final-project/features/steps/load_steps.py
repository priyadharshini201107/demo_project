from behave import given, when, then


@given("the product service is running")
def step_service_running(context):
    context.response = None


@when('I create a product named "{name}"')
def step_create_product(context, name):
    context.response = context.client.post("/products", json={"name": name})


@then("the product should be available in the catalogue")
def step_product_available(context):
    assert context.response.status_code == 201
    product_id = context.response.get_json()["id"]
    response = context.client.get(f"/products/{product_id}")
    assert response.status_code == 200
