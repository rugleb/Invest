from datetime import date
from http import HTTPStatus
from typing import Callable

import pytest
from aiohttp.test_utils import TestClient

from invest_api import Company
from invest_api.utils import is_valid_uuid


class TestPingView:
    url = "/ping"

    async def test_that_route_is_named(self, client: TestClient) -> None:
        url = client.app.router["ping"].url_for()

        assert self.url == str(url)

    async def test_that_service_is_alive(self, client: TestClient) -> None:
        response = await client.get(self.url)
        assert response.status == HTTPStatus.OK

        assert await response.json() == {
            "data": None,
            "message": "pong",
        }

        request_id = response.headers.get("X-Request-ID")
        assert is_valid_uuid(request_id)


class TestHealthView:
    url = "/health"

    async def test_that_route_is_named(self, client: TestClient) -> None:
        url = client.app.router["health"].url_for()

        assert self.url == str(url)

    async def test_that_service_is_alive(self, client: TestClient) -> None:
        response = await client.get(self.url)
        assert response.status == HTTPStatus.OK

        assert await response.json() == {
            "data": None,
            "message": "OK",
        }

        request_id = response.headers.get("X-Request-ID")
        assert is_valid_uuid(request_id)


class TestCompanyView:
    url = "/companies/{id}"

    async def test_that_route_is_named(self, client: TestClient) -> None:
        identifier = "7710561081"
        url = client.app.router["company"].url_for(id=identifier)

        assert self.url.format(id=identifier) == str(url)

    async def test_request_with_not_existing_company(
            self,
            client: TestClient,
    ) -> None:
        identifier = "8887776655"
        url = self.url.format(id=identifier)

        response = await client.get(url)
        assert response.status == HTTPStatus.NOT_FOUND

        assert await response.json() == {
            "message": "Not found",
        }

    @pytest.mark.parametrize("identifier_key", [
        "itn",
        "psrn",
    ])
    async def test_request_with_existing_company(
            self,
            client: TestClient,
            create_company: Callable,
            identifier_key: str,
    ) -> None:
        company = Company(
            id=1,
            name="ЗАО ОКБ",
            size="Крупная",
            registered_at=date(2010, 1, 1),
            itn="7710561081",
            psrn="1047796788819",
            region_code="77",
            region_name="Москва",
            activity_code="5",
            activity_name="Высокая",
            charter_capital=1200,
            is_acting=True,
            is_liquidating=False,
            not_reported_last_year=True,
            not_in_sme_registry=False,
            ceo_has_other_companies=True,
            negative_list_risk=False,
            bankruptcy_probability=5,
            bankruptcy_vars=None,
            is_enough_finance_data=True,
            relative_success=7,
            revenue_forecast=25000,
            assets_forecast=20000,
            dev_stage="Развивается активно",
            dev_stage_coordinates=None,
        )
        create_company(company)

        identifier = getattr(company, identifier_key)
        url = self.url.format(id=identifier)

        response = await client.get(url)
        assert response.status == HTTPStatus.OK

        data = company.to_dict()

        assert await response.json() == {
            "data": data,
            "message": "OK",
        }


class TestCompaniesView:
    url = "/companies"

    async def test_that_route_is_named(self, client: TestClient) -> None:
        url = client.app.router["companies"].url_for()

        assert self.url == str(url)

    async def test_request_without_query_params(
            self,
            client: TestClient,
    ) -> None:
        response = await client.get(self.url)
        assert response.status == HTTPStatus.UNPROCESSABLE_ENTITY

        assert await response.json() == {
            "errors": {
                "name": ["Missing data for required field."],
            },
            "message": "Input payload validation failed",
        }

    async def test_request_with_undefined_company_name(
            self,
            client: TestClient,
    ) -> None:
        params = {
            "name": "undefined",
        }

        response = await client.get(self.url, params=params)
        assert response.status == HTTPStatus.OK

        assert await response.json() == {
            "data": [],
            "message": "OK",
        }

    async def test_request_with_existing_company_name(
            self,
            client: TestClient,
            create_company: Callable,
    ) -> None:
        company = Company(
            id=1,
            name="ОАО Ёжики и Грибочки",
            size="Микропредприятие",
            registered_at=date(2010, 1, 1),
            itn="2464222938",
            psrn="1102454000670",
            region_code="77",
            region_name="Москва",
            activity_code="47.51.1",
            activity_name="Семейный подряд",
            charter_capital=1000,
            is_acting=True,
            is_liquidating=False,
            not_reported_last_year=True,
            not_in_sme_registry=False,
            ceo_has_other_companies=True,
            negative_list_risk=False,
            bankruptcy_probability=5,
            bankruptcy_vars=None,
            is_enough_finance_data=True,
            relative_success=7,
            revenue_forecast=25000,
            assets_forecast=20000,
            dev_stage="Рост активов",
            dev_stage_coordinates=None,
        )
        create_company(company)

        params = {
            "name": "ежеки",
        }

        response = await client.get(self.url, params=params)
        assert response.status == HTTPStatus.OK

        assert await response.json() == {
            "data": [
                company.to_dict(),
            ],
            "message": "OK",
        }
