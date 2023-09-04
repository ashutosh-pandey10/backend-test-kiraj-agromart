import asyncio
from .models import Candle, ConvertedCandle

async def async_convert_candles(candles, timeframe):
    """
    Asynchronously convert one-minute candles to the specified timeframe.
    """
    converted_candles = []
    current_timeframe = None
    open_price = None
    high_price = None
    low_price = None
    close_price = None
    candle_date = None

    for candle in candles:
        if current_timeframe is None:
            current_timeframe = candle.date
            open_price = candle.open
            high_price = candle.high
            low_price = candle.low
            close_price = candle.close
            candle_date = candle.date
        elif (candle.date - current_timeframe).total_seconds() < (timeframe * 60):
            # Update high and low prices within the timeframe
            high_price = max(high_price, candle.high)
            low_price = min(low_price, candle.low)
            close_price = candle.close
        else:
            # Create a new candle for the specified timeframe
            new_candle = ConvertedCandle(
                open=open_price,
                high=high_price,
                low=low_price,
                close=close_price,
                date=candle_date
            )
            converted_candles.append(new_candle)
            # Reset for the next timeframe
            current_timeframe = candle.date
            open_price = candle.open
            high_price = candle.high
            low_price = candle.low
            close_price = candle.close
            candle_date = candle.date

    # Create a new candle for the last timeframe
    if current_timeframe is not None:
        new_candle = ConvertedCandle(
            open=open_price,
            high=high_price,
            low=low_price,
            close=close_price,
            date=candle_date
        )
        converted_candles.append(new_candle)

    return converted_candles

async def async_process_candles(candles, timeframe):
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, async_convert_candles, candles, timeframe)
