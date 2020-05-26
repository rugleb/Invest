from datetime import date
from http import HTTPStatus
from typing import Callable

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
            "data": {},
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
            "data": {},
            "message": "OK",
        }

        request_id = response.headers.get("X-Request-ID")
        assert is_valid_uuid(request_id)


class TestCompanyView:
    url = "/companies/{itn}"

    async def test_that_route_is_named(self, client: TestClient) -> None:
        itn = "7710561081"
        url = client.app.router["company"].url_for(itn=itn)

        assert self.url.format(itn=itn) == str(url)

    async def test_request_with_not_existing_company(
            self,
            client: TestClient,
    ) -> None:
        itn = "8887776655"
        url = self.url.format(itn=itn)

        response = await client.get(url)
        assert response.status == HTTPStatus.NOT_FOUND

        assert await response.json() == {
            "message": "Not found",
        }

    async def test_request_with_existing_company(
            self,
            client: TestClient,
            create_company: Callable,
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

        url = self.url.format(itn=company.itn)

        response = await client.get(url)
        assert response.status == HTTPStatus.OK

        data = {
            "id": company.id,
            "name": company.name,
            "size": company.size,
            "registered_at": company.registered_at.strftime("%Y-%m-%d"),
            "itn": company.itn,
            "psrn": company.psrn,
            "region_code": company.region_code,
            "region_name": company.region_name,
            "activity_code": company.activity_code,
            "activity_name": company.activity_name,
            "charter_capital": company.charter_capital,
            "is_acting": company.is_acting,
            "is_liquidating": company.is_liquidating,
            "not_reported_last_year": company.not_reported_last_year,
            "not_in_sme_registry": company.not_in_sme_registry,
            "ceo_has_other_companies": company.ceo_has_other_companies,
            "negative_list_risk": company.negative_list_risk,
            "bankruptcy_probability": company.bankruptcy_probability,
            "bankruptcy_vars": company.bankruptcy_vars,
            "is_enough_finance_data": company.is_enough_finance_data,
            "relative_success": company.relative_success,
            "revenue_forecast": company.revenue_forecast,
            "assets_forecast": company.assets_forecast,
            "dev_stage": company.dev_stage,
            "dev_stage_coordinates": company.dev_stage_coordinates,
        }

        assert await response.json() == {
            "data": data,
            "message": "OK",
        }
