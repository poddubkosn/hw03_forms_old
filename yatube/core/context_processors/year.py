import datetime as dt


def year(request):
    """Добавляет переменную с текущим годом."""
    now = dt.datetime.now()
    date = now.year
    return {'year': date}
