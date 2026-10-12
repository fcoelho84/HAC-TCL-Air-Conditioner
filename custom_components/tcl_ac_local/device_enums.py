"""."""

import logging
from enum import StrEnum

_LOGGER = logging.getLogger(__name__)


class ModeEnum(StrEnum):
    COOL = "Frio"
    HEAT = "Calor"
    DEHUMIDIFICATION = "Desumidificação"
    FAN = "Ventilação"
    AUTO = "Automático"


class DehumidifierModeEnum(StrEnum):
    DRY = "Seco"
    TURBO = "Turbo"
    COMFORT = "Conforto"
    CONTINUE = "Contínuo"


class UpAndDownAirSupplyVectorEnum(StrEnum):
    UP_AND_DOWN_SWING = "Oscilação vertical"
    UPWARDS_SWING = "Oscilação para cima"
    DOWNWARDS_SWING = "Oscilação para baixo"
    TOP_FIX = "Fixo no topo"
    UPPER_FIX = "Fixo em cima"
    MIDDLE_FIX = "Fixo no meio"
    LOWER_FIX = "Fixo embaixo"
    BOTTOM_FIX = "Fixo na base"
    NOT_SET = "Não definido"


def getUpAndDownAirSupplyVector(
    vertical_direction: int | float,
) -> UpAndDownAirSupplyVectorEnum:
    match vertical_direction:
        case 1:
            return UpAndDownAirSupplyVectorEnum.UP_AND_DOWN_SWING
        case 2:
            return UpAndDownAirSupplyVectorEnum.UPWARDS_SWING
        case 3:
            return UpAndDownAirSupplyVectorEnum.DOWNWARDS_SWING
        case 8:
            return UpAndDownAirSupplyVectorEnum.NOT_SET
        case 9:
            return UpAndDownAirSupplyVectorEnum.TOP_FIX
        case 10:
            return UpAndDownAirSupplyVectorEnum.UPPER_FIX
        case 11:
            return UpAndDownAirSupplyVectorEnum.MIDDLE_FIX
        case 12:
            return UpAndDownAirSupplyVectorEnum.LOWER_FIX
        case 13:
            return UpAndDownAirSupplyVectorEnum.BOTTOM_FIX


class LeftAndRightAirSupplyVectorEnum(StrEnum):
    LEFT_AND_RIGHT_SWING = "Oscilação horizontal"
    LEFT_SWING = "Oscilação à esquerda"
    MIDDLE_SWING = "Oscilação no meio"
    RIGHT_SWING = "Oscilação à direita"
    LEFT_FIX = "Fixo à esquerda"
    CENTER_LEFT_FIX = "Fixo centro-esquerda"
    MIDDLE_FIX = "Fixo no meio"
    CENTER_RIGHT_FIX = "Fixo centro-direita"
    RIGHT_FIX = "Fixo à direita"
    NOT_SET = "Não definido"


def getLeftAndRightAirSupplyVector(
    horizontal_direction: int | float,
) -> LeftAndRightAirSupplyVectorEnum:
    match horizontal_direction:
        case 1:
            return LeftAndRightAirSupplyVectorEnum.LEFT_AND_RIGHT_SWING
        case 2:
            return LeftAndRightAirSupplyVectorEnum.LEFT_SWING
        case 3:
            return LeftAndRightAirSupplyVectorEnum.MIDDLE_SWING
        case 4:
            return LeftAndRightAirSupplyVectorEnum.RIGHT_SWING
        case 8:
            return LeftAndRightAirSupplyVectorEnum.NOT_SET
        case 9:
            return LeftAndRightAirSupplyVectorEnum.LEFT_FIX
        case 10:
            return LeftAndRightAirSupplyVectorEnum.CENTER_LEFT_FIX
        case 11:
            return LeftAndRightAirSupplyVectorEnum.MIDDLE_FIX
        case 12:
            return LeftAndRightAirSupplyVectorEnum.CENTER_RIGHT_FIX
        case 13:
            return LeftAndRightAirSupplyVectorEnum.RIGHT_FIX


class SleepModeEnum(StrEnum):
    STANDARD = "Padrão"
    ELDERLY = "Idoso"
    CHILD = "Criança"
    OFF = "Desligado"


def getSleepMode(sleep: int | float) -> SleepModeEnum:
    match sleep:
        case 1:
            return SleepModeEnum.STANDARD
        case 2:
            return SleepModeEnum.ELDERLY
        case 3:
            return SleepModeEnum.CHILD
        case 0:
            return SleepModeEnum.OFF


class WindSeed7GearEnum(StrEnum):
    TURBO = "Turbo"
    AUTO = "Automático"
    SPEED_1 = "1"
    SPEED_2 = "2"
    SPEED_3 = "3"
    SPEED_4 = "4"
    SPEED_5 = "5"
    SPEED_6 = "6"


def getWindSeed7Gear(wind_speed_7_gear: int) -> WindSeed7GearEnum:
    match wind_speed_7_gear:
        case 1:
            return WindSeed7GearEnum.SPEED_1
        case 2:
            return WindSeed7GearEnum.SPEED_2
        case 3:
            return WindSeed7GearEnum.SPEED_3
        case 4:
            return WindSeed7GearEnum.SPEED_4
        case 5:
            return WindSeed7GearEnum.SPEED_5
        case 6:
            return WindSeed7GearEnum.SPEED_6
        case 7:
            return WindSeed7GearEnum.TURBO
        case 0:
            return WindSeed7GearEnum.AUTO
        case _:
            return WindSeed7GearEnum.AUTO


class WindSeedEnum(StrEnum):
    STRONG = "Forte"
    HIGH = "Alta"
    MID_HIGH = "Média-alta"
    MEDIUM = "Média"
    MID_LOW = "Média-baixa"
    LOW = "Baixa"
    MUTE = "Mudo"
    AUTO = "Automático"


def getWindSpeed(wind_speed: int, turbo: int, silence_switch: int) -> WindSeedEnum:
    match wind_speed:
        case 6:
            return WindSeedEnum.STRONG if turbo == 1 else WindSeedEnum.HIGH
        case 5:
            return WindSeedEnum.MID_HIGH
        case 4:
            return WindSeedEnum.MEDIUM
        case 3:
            return WindSeedEnum.MID_LOW
        case 2:
            return WindSeedEnum.MUTE if silence_switch == 1 else WindSeedEnum.LOW
        case 0:
            return WindSeedEnum.AUTO
        case _:
            return WindSeedEnum.AUTO


class PortableWindSeedEnum(StrEnum):
    HIGH = "Alta"
    LOW = "Baixa"
    AUTO = "Automático"


def getPortableWindSeed(wind_speed: int, has_auto_mode: bool) -> PortableWindSeedEnum:
    if has_auto_mode:
        match wind_speed:
            case 2:
                return PortableWindSeedEnum.HIGH
            case 1:
                return PortableWindSeedEnum.LOW
            case 0:
                return PortableWindSeedEnum.AUTO
            case _:
                return PortableWindSeedEnum.AUTO
    else:
        match wind_speed:
            case 1:
                return PortableWindSeedEnum.HIGH
            case 0:
                return PortableWindSeedEnum.LOW
            case _:
                return PortableWindSeedEnum.LOW


class PortableWind4ValueSeedEnum(StrEnum):
    HIGH = "Alta"
    MEDIUM = "Média"
    LOW = "Baixa"
    AUTO = "Automático"


def getPortableWind4ValueSeed(
    wind_speed: int, has_auto_mode: bool = False
) -> PortableWind4ValueSeedEnum:
    if has_auto_mode:
        match wind_speed:
            case 3:
                return PortableWind4ValueSeedEnum.HIGH
            case 2:
                return PortableWind4ValueSeedEnum.MEDIUM
            case 1:
                return PortableWind4ValueSeedEnum.LOW
            case 0:
                return PortableWind4ValueSeedEnum.AUTO
            case _:
                return PortableWind4ValueSeedEnum.AUTO
    else:
        match wind_speed:
            case 2:
                return PortableWind4ValueSeedEnum.HIGH
            case 1:
                return PortableWind4ValueSeedEnum.MEDIUM
            case 0:
                return PortableWind4ValueSeedEnum.LOW
            case _:
                return PortableWind4ValueSeedEnum.LOW


class WindowAcWindSeedEnum(StrEnum):
    SPEED_1 = "1"
    SPEED_2 = "2"
    SPEED_3 = "3"
    AUTO = "Automático"


def getWindowAcWindSeed(wind_speed: int) -> PortableWindSeedEnum:
    match wind_speed:
        case 2:
            return WindowAcWindSeedEnum.SPEED_1
        case 4:
            return WindowAcWindSeedEnum.SPEED_2
        case 6:
            return WindowAcWindSeedEnum.SPEED_3
        case _:
            return WindowAcWindSeedEnum.AUTO


class TemperatureTypeEnum(StrEnum):
    FAHRENHEIT = "Fahrenheit"
    CELSIUS = "Celsius"


def getTemperatureType(temperature_type: int) -> TemperatureTypeEnum:
    match temperature_type:
        case 1:
            return TemperatureTypeEnum.FAHRENHEIT
        case 0:
            return TemperatureTypeEnum.CELSIUS
        case _:
            return TemperatureTypeEnum.CELSIUS


class FreshAirEnum(StrEnum):
    AUTO = "Automático"
    STRENGTH_1 = "1"
    STRENGTH_2 = "2"
    STRENGTH_3 = "3"


def getFreshAir(new_wind_strength: int) -> FreshAirEnum:
    match new_wind_strength:
        case 1:
            return FreshAirEnum.STRENGTH_1
        case 2:
            return FreshAirEnum.STRENGTH_2
        case 3:
            return FreshAirEnum.STRENGTH_3
        case 0:
            return FreshAirEnum.AUTO
        case _:
            return FreshAirEnum.AUTO


class WindFeelingEnum(StrEnum):
    NONE = "Não definido"
    SOFT = "Suave"
    SHOWER = "Chuveiro"
    CARPET = "Carpete"
    SURROUND = "Envolvente"


def getWindFeeling(soft_wind: int) -> WindFeelingEnum:
    match soft_wind:
        case 1:
            return WindFeelingEnum.SOFT
        case 2:
            return WindFeelingEnum.SHOWER
        case 3:
            return WindFeelingEnum.CARPET
        case 3:
            return WindFeelingEnum.SURROUND
        case 0:
            return WindFeelingEnum.NONE
        case _:
            return WindFeelingEnum.NONE


class GeneratorModeEnum(StrEnum):
    NONE = "Não definido"
    L1 = "L1 30%"
    L2 = "L2 50%"
    L3 = "L3 70%"


def getGeneratorMode(generator_mode: int) -> GeneratorModeEnum:
    match generator_mode:
        case 1:
            return GeneratorModeEnum.L1
        case 2:
            return GeneratorModeEnum.L2
        case 3:
            return GeneratorModeEnum.L3
        case 0:
            return GeneratorModeEnum.NONE


class WindSpeedLowMediumHigh(StrEnum):
    LOW = "Baixa"
    MEDIUM = "Média"
    HIGH = "Alta"


def getWindSpeedLowMediumHigh(windSpeed: int) -> GeneratorModeEnum:
    match windSpeed:
        case 0:
            return WindSpeedLowMediumHigh.LOW
        case 1:
            return WindSpeedLowMediumHigh.MEDIUM
        case 2:
            return WindSpeedLowMediumHigh.HIGH
    return GeneratorModeEnum.LOW


class AirPurifierFanWindSpeedEnum(StrEnum):
    LOW = "1"
    MEDIUM = "2"
    HIGH = "3"


class AirPurifierWorkModeEnum(StrEnum):
    AUTO = "0"
    SLEEP = "1"
    FAN = "2"


class AirPurifierFanWindSpeedStrEnum(StrEnum):
    LOW = "Baixa"
    MEDIUM = "Média"
    HIGH = "Alta"


class AirPurifierWorkModeStrEnum(StrEnum):
    AUTO = "Automático"
    FAN = "Ventilação"
    SLEEP = "Sono"


def getAirPurifierFanWindSpeed(windSpeed: int) -> AirPurifierFanWindSpeedEnum:
    match windSpeed:
        case 1:
            return AirPurifierFanWindSpeedStrEnum.LOW
        case 2:
            return AirPurifierFanWindSpeedStrEnum.MEDIUM
        case 3:
            return AirPurifierFanWindSpeedStrEnum.HIGH
    return AirPurifierFanWindSpeedStrEnum.LOW


def getAirPurifierWorkMode(workMode: int) -> AirPurifierWorkModeEnum:
    match workMode:
        case 0:
            return AirPurifierWorkModeStrEnum.AUTO
        case 1:
            return AirPurifierWorkModeStrEnum.SLEEP
        case 2:
            return AirPurifierWorkModeStrEnum.FAN
    return AirPurifierWorkModeStrEnum.AUTO
