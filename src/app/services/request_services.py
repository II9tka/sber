import httpx

from decimal import Decimal
from xml.etree import ElementTree

from app.settings import CBR_URL, FORMATS
from .dataclasses.cbr import ValCursDataClass, ValuteDataClass
from .dataclasses.response import Response
from ..utils.convert import from_str_date_to_datetime


async def get_cbr(date: str):
    try:
        response = httpx.get(
            CBR_URL,
            params={'date_req': from_str_date_to_datetime(date).strftime(FORMATS['DATE_CBR_REQUEST_FORMAT'])}
        )
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        return Response(has_errors=True, error=str(e))

    content = response.content.decode('windows-1251')
    root = ElementTree.fromstring(content)

    val_curs = ValCursDataClass(
        request_date=from_str_date_to_datetime(date),
        date=from_str_date_to_datetime(root.get('Date'), date_format=FORMATS['DATE_CBR_RESPONSE_FORMAT']),
        name=root.get('name'),
        valutes=[]
    )

    for valute in root.iter('Valute'):
        alter_id = valute.get('ID')

        num_code = valute.find('NumCode').text
        char_code = valute.find('CharCode').text
        nominal = valute.find('Nominal').text
        name = valute.find('Name').text
        value = Decimal(valute.find('Value').text.replace(',', '.'))

        val_curs.valutes.append(ValuteDataClass(
            alter_id=alter_id,
            num_code=num_code,
            char_code=char_code,
            nominal=nominal,
            name=name,
            value=value
        ))

    return Response(val_curs=val_curs)
