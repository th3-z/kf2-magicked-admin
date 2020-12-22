from collections import namedtuple

CHAT_MAX_ROWS = 7
CHAT_MAX_COLUMNS = 21

DIFF_UNKNOWN = "-1.0000"
DIFF_NORM = "0.0000"
DIFF_HARD = "1.0000"
DIFF_SUI = "2.0000"
DIFF_HOE = "3.0000"
DIFF_DISPLAY = {
    DIFF_UNKNOWN: "Unknown",
    DIFF_NORM: "Normal",
    DIFF_HARD: "Hard",
    DIFF_SUI: "Suicidal",
    DIFF_HOE: "HoE"
}

LEN_UNKNOWN = 0
LEN_SHORT = 4
LEN_NORM = 7
LEN_LONG = 10
LEN_DISPLAY = {
    LEN_UNKNOWN: "Unknown",
    LEN_SHORT: "Short",
    LEN_NORM: "Normal",
    LEN_LONG: "Long"
}

GAME_TYPE_UNKNOWN = "kfgamecontent.KFGameInfo_Unknown"
GAME_TYPE_SURVIVAL = "kfgamecontent.KFGameInfo_Survival"
GAME_TYPE_WEEKLY = "kfgamecontent.KFGameInfo_WeeklySurvival"
GAME_TYPE_SURVIVAL_VS = "kfgamecontent.KFGameInfo_VersusSurvival"
GAME_TYPE_ENDLESS = "kfgamecontent.KFGameInfo_Endless"
GAME_TYPE_OBJECTIVE = "kfgamecontent.KFGameInfo_Objective"
GAME_TYPE_KF1 = "KF1.KF1_GameInfo"
GAME_TYPE_ZEDTERNAL = "Zedternal.WMGameInfo_Endless"
GAME_TYPE_ZEDTERNAL_ALLWEAPONS = "Zedternal.WMGameInfo_Endless_AllWeapons"
GAME_TYPE_ZEDTERNAL_REBORN = "ZedternalReborn.WMGameInfo_Endless"
GAME_TYPE_ZEDTERNAL_REBORN_ALLWEAPONS = "ZedternalReborn.WMGameInfo_Endless_AllWeapons"
GAME_TYPE_CONTROLLED_DIFFICULTY_ETERNAL = "ControlledDifficulty_Eternal.CD_Survival"
GAME_TYPE_CONTROLLED_DIFFICULTY_ETERNAL_SHOOTING_VERSION = "ControlledDifficulty_Eternal.CD_ShootingSurvival"
GAME_TYPE_CONTROLLED_DIFFICULTY_ENDLESS = "ControlledDifficulty_Endless.CD_Endless"
GAME_TYPE_SCRAKEMONIUM_OUTBREAK = "Scrakemonium.KFGameInfo_Scrakemonium"
GAME_TYPE_ZED_SURVIVAL_VS = "ZombieVS.VSGame"
GAME_TYPE_ENDLESS_SPECIAL_WAVES_ONLY = "Endless_Tweaks.KFGameInfo_EndlessTweaks"
GAME_TYPE_FLYING_EDARS_SURVIVAL = "DAR.DARGameInfo_Survival"
GAME_TYPE_FLYING_EDARS_ENDLESS = "DAR.DARGameInfo_Endless"
GAME_TYPE_RISE_OF_THE_MACHINES = "Machines.KFGameInfo_Machines"
GAME_TYPE_BOSSAPALOOZA = "Bossapalooza.KFGameinfo_Boss"
GAME_TYPE_SETWAVE_ENDLESS = "SetWave.SWGameInfo_Endless"
GAME_TYPE_SIMPLY_ENDLESS = "SimplyEndless.SimplyEndless"
GAME_TYPE_LIGHTS_OUT = "LightsOut.LightsOut_Gameinfo"
GAME_TYPE_LIGHTS_OUT_INFINITE_FLASHLIGHT = "LightsOutInfinite.LightsOutInf_Gameinfo"
GAME_TYPE_HEADSHOT_COUNTER_SURVIVAL = "HeadshotCounter.HeadshotCounter_Survival"
GAME_TYPE_HEADSHOT_COUNTER_ENDLESS = "HeadshotCounter.HeadshotCounter_Endless"
GAME_TYPE_HEADSHOT_COUNTER_WEEKLY = "HeadshotCounter.HeadshotCounter_Weekly"
GAME_TYPE_POUNDAMONIUM = "Poundamonium.KFGameinfo_Pound"
GAME_TYPE_BOSS_WAVES = "BossChallenge.KFGameInfo_BossChallenge"
GAME_TYPE_DODGE_IT = "ZedtimeMod.KFGameInfo_ZedtimeMod"
GAME_TYPE_MINIPATTIES_VERSUS_CHALLENGE = "Versus_Tweaks.KFGameInfo_VersusT"
GAME_TYPE_CONFIGURABLE_OBJECTIVE = "CollectObj.KFGameInfo_CollectObj"
GAME_TYPE_KNOCK_IT = "ZedtimeModSwat.KFGameInfo_ZedtimeModSwat"
GAME_TYPE_PLAY_DEMO_LIKE_A_PRO = "RPGScrake.KFGameInfo_RPGScrakeMod"
GAME_TYPE_NUKED = "ZedtimeModNuked.KFGameInfo_ZedtimeModNuked"
GAME_TYPE_HARD_MODE_BOSS = "HardModeBoss.HardSurv"
GAME_TYPE_KNIFE_AND_9MM_ONLY = "MeleeOnlyMutator.MeleeOnly"
GAME_TYPE_CYBERDEMON_HUSK = "Cyberdemon.KFGameInfo_SurvivalCyberdemon"
GAME_TYPE_HELLKNIGHT_FLESHPOUND = "HellknightZed.KFGameInfo_SurvivalHellknight"
GAME_TYPE_PEST_ZOMBIE_SIREN = "PestZed.KFGameInfo_SurvivalPest"
GAME_TYPE_REVENANT_HUSK = "Revenant.KFGameInfo_SurvivalRevenant"
GAME_TYPE_GNAAR_ZOMBIE_GOREFIEND = "GnaarZed.KFGameInfo_SurvivalGnaar"
GAME_TYPE_MANCUBUS_HUSK = "Mancubus.KFGameInfo_SurvivalMancubus"
GAME_TYPE_ARCHVILE_ALPHACLOT = "Archvile.KFGameInfo_SurvivalArchvile"
GAME_TYPE_EXTENDED_WEEKLIES_RADOM = "ExtendedWeeklies.Random"
GAME_TYPE_EXTENDED_WEEKLIES_HARDCORE_SCAVENGER = "ExtendedWeeklies.HardcoreScavenger"
GAME_TYPE_EXTENDED_WEEKLIES_NO_DARS = "ExtendedWeeklies.NoDars"
GAME_TYPE_EXTENDED_WEEKLIES_NO_DARS_ALLOWED = "ExtendedWeeklies.NoDarsAllowed"
GAME_TYPE_EXTENDED_WEEKLIES_WACKY_ROCKETEERS = "ExtendedWeeklies.WackyRocketeers"
GAME_TYPE_EXTENDED_WEEKLIES_CLASSIC = "ExtendedWeeklies.Classic"
GAME_TYPE_EXTENDED_WEEKLIES_SCAVENGER = "ExtendedWeeklies.Scavenger"
GAME_TYPE_EXTENDED_WEEKLIES_RAMBO = "ExtendedWeeklies.Rambo"
GAME_TYPE_EXTENDED_WEEKLIES_POUNDEMIC = "ExtendedWeeklies.Poundemic"
GAME_TYPE_EXTENDED_WEEKLIES_POODEMONIUM = "ExtendedWeeklies.Poodemonium"
GAME_TYPE_BIG_HEAD = "BigHeads.KFGameInfo_BigHeads"
GAME_TYPE_FIESTA = "Fiesta.Fiesta"
GAME_TYPE_CLASSIC_MODE = "KFClassicModeSrv.ClassicMode"
GAME_TYPE_POUNDAMONIUM_OUTBREAK = "Poundamonium.KFGameInfo_Poundamonium"
GAME_TYPE_POUNDAMONIUM_OUTBREAK_HARD = "Poundamonium.KFGameInfo_PoundamoniumHard"
GAME_TYPE_POUNDAMONIUM_OUTBREAK_CLASSIC = "Poundamonium.KFGameInfo_PoundamoniumClassic"
GAME_TYPE_LEAGUE_OF_ZEDS = "League.Survival_LOZ"
GAME_TYPE_THE_HUSK_FLOOR = "KFHuskSurvival.KFGameInfo_HuskSurvival"
GAME_TYPE_REALISM_OBJECTIVE_MOD = "CollectObjSc.KFGameInfo_CollectObjSc"
GAME_TYPE_BOOM_WEEKLY_OUTBREAK_STANDALONE = "KFGameInfo_Boom"
GAME_TYPE_BOOM_WEEKLY_OUTBREAK_STANDALONE_V2 = "KFGameInfo_BoomV2"
GAME_TYPE_BOBBLE_ZEDS_WEEKLY_OUTBREAK_STANDALONE = "BobbleZed.KFGameInfo_BobbleZed"
GAME_TYPE_BOBBLE_ZEDS_WEEKLY_OUTBREAK_STANDALONE_V2 = "BobbleZed.KFGameInfo_BobbleZedV2"
GAME_TYPE_ZED_TIME_WEEKLY_OUTBREAK_STANDALONE = "ZedTime.KFGameInfo_ZedTime"
GAME_TYPE_ZED_TIME_WEEKLY_OUTBREAK_STANDALONE_V2 = "ZedTime.KFGameInfo_ZedTimeV2"
GAME_TYPE_TINY_TERROR_WEEKLY_OUTBREAK_STANDALONE = "TinyTerror.KFGameInfo_TinyTerror"
GAME_TYPE_TINY_TERROR_WEEKLY_OUTBREAK_STANDALONE_V2 = "TinyTerror.KFGameInfo_TinyTerrorV2"
GAME_TYPE_CRANIUM_CRACKER_WEEKLY_OUTBREAK_STANDALONE = "CraniumCracker.KFGameInfo_CraniumCracker"
GAME_TYPE_CRANIUM_CRACKER_WEEKLY_OUTBREAK_STANDALONE_V2 = "CraniumCracker.KFGameInfo_CraniumCrackerV2"
GAME_TYPE_DUMMY_MOD = "DummyMod.Dummy_Survival"
GAME_TYPE_CONTROLLED_DIFFICULTY_BLACKOUT = "ControlledDifficulty_Blackout.CD_Survival"
GAME_TYPE_ELITE_VERSUS = "KFPVPElite.KFGameInfo_VersusSurvivalEx"
GAME_TYPE_CONTROLLED_DIFFICULTY = "ControlledDifficulty.CD_Survival"
GAME_TYPE_ABOMINATIONS_MINIBOSSES_SPAWN = "KBMiniBossesMod.KFGameInfo_KBMiniBosses"
GAME_TYPE_DISPLAY = {
    GAME_TYPE_UNKNOWN: "Unknown",
    GAME_TYPE_SURVIVAL: "Survival",
    GAME_TYPE_WEEKLY: "Weekly",
    GAME_TYPE_SURVIVAL_VS: "Versus Survival",
    GAME_TYPE_ENDLESS: "Endless",
    GAME_TYPE_OBJECTIVE: "Objective",
    GAME_TYPE_KF1: "KF1 Gamemode",
    GAME_TYPE_ZEDTERNAL: "Zedternal",
    GAME_TYPE_ZEDTERNAL_ALLWEAPONS: "Zedternal AllWeapons",
    GAME_TYPE_ZEDTERNAL_REBORN: "Zedternal Reborn",
    GAME_TYPE_ZEDTERNAL_REBORN_ALLWEAPONS: "Zedternal Reborn AllWeapons",
    GAME_TYPE_CONTROLLED_DIFFICULTY_ETERNAL: "Controlled Difficulty Eternal Survival",
    GAME_TYPE_CONTROLLED_DIFFICULTY_ETERNAL_SHOOTING_VERSION: "Controlled Difficulty Eternal Survival - Shooting Only",
    GAME_TYPE_CONTROLLED_DIFFICULTY_ENDLESS: "Controlled Difficulty Endless",
    GAME_TYPE_SCRAKEMONIUM_OUTBREAK: "Scrakemonium Outbreak",
    GAME_TYPE_ZED_SURVIVAL_VS: "ZEDs Survival VS",
    GAME_TYPE_ENDLESS_SPECIAL_WAVES_ONLY: "Endless Special Waves Only",
    GAME_TYPE_FLYING_EDARS_SURVIVAL: "Flying EDARs Survival",
    GAME_TYPE_FLYING_EDARS_ENDLESS: "Flying EDARs Endless",
    GAME_TYPE_RISE_OF_THE_MACHINES: "Rise of the Machines",
    GAME_TYPE_BOSSAPALOOZA: "Bossapalooza",
    GAME_TYPE_SETWAVE_ENDLESS: "SetWave Endless",
    GAME_TYPE_SIMPLY_ENDLESS: "Simply Endless",
    GAME_TYPE_LIGHTS_OUT: "Lights Out",
    GAME_TYPE_LIGHTS_OUT_INFINITE_FLASHLIGHT: "Lights Out Infinite Flashlight / NV Version",
    GAME_TYPE_HEADSHOT_COUNTER_SURVIVAL: "Headshot Counter Survival",
    GAME_TYPE_HEADSHOT_COUNTER_ENDLESS: "Headshot Counter Endless",
    GAME_TYPE_HEADSHOT_COUNTER_WEEKLY: "Headshot Counter Weekly",
    GAME_TYPE_POUNDAMONIUM: "Poundamonium",
    GAME_TYPE_BOSS_WAVES: "Boss Waves",
    GAME_TYPE_DODGE_IT: "Dodge It",
    GAME_TYPE_MINIPATTIES_VERSUS_CHALLENGE: "Minipatties VS Challenge",
    GAME_TYPE_CONFIGURABLE_OBJECTIVE: "Configurable Objective",
    GAME_TYPE_KNOCK_IT: "Knock It",
    GAME_TYPE_PLAY_DEMO_LIKE_A_PRO: "Play Demo like a Pro - RPG / Scrake",
    GAME_TYPE_NUKED: "Nuked",
    GAME_TYPE_HARD_MODE_BOSS: "Hard Mode Boss",
    GAME_TYPE_KNIFE_AND_9MM_ONLY: "Knife and 9mm Only",
    GAME_TYPE_CYBERDEMON_HUSK: "Cyberdemon Husk",
    GAME_TYPE_HELLKNIGHT_FLESHPOUND: "Hellknight FleshPound",
    GAME_TYPE_PEST_ZOMBIE_SIREN: "Pest Siren",
    GAME_TYPE_REVENANT_HUSK: "Revenant Husk",
    GAME_TYPE_GNAAR_ZOMBIE_GOREFIEND: "Gnaar Zombie Gorefiend",
    GAME_TYPE_MANCUBUS_HUSK: "Mancubus Husk",
    GAME_TYPE_ARCHVILE_ALPHACLOT: "Archvile Alphaclot",
    GAME_TYPE_EXTENDED_WEEKLIES_RADOM: "Extended Weeklies Random",
    GAME_TYPE_EXTENDED_WEEKLIES_HARDCORE_SCAVENGER: "Extended Weeklies Hardcore Scavenger",
    GAME_TYPE_EXTENDED_WEEKLIES_NO_DARS: "Extended Weeklies NoDars",
    GAME_TYPE_EXTENDED_WEEKLIES_NO_DARS_ALLOWED: "Extended Weeklies NoDars Allowed",
    GAME_TYPE_EXTENDED_WEEKLIES_WACKY_ROCKETEERS: "Extended Weeklies Wacky Rocketeers",
    GAME_TYPE_EXTENDED_WEEKLIES_CLASSIC: "Extended Weeklies Classic",
    GAME_TYPE_EXTENDED_WEEKLIES_SCAVENGER: "Extended Weeklies Scavenger",
    GAME_TYPE_EXTENDED_WEEKLIES_RAMBO: "Extended Weeklies Rambo",
    GAME_TYPE_EXTENDED_WEEKLIES_POUNDEMIC: "Extended Weeklies Poundemic",
    GAME_TYPE_EXTENDED_WEEKLIES_POODEMONIUM: "Extended Weeklies Poodemonium",
    GAME_TYPE_BIG_HEAD: "Big Head",
    GAME_TYPE_FIESTA: "Fiesta",
    GAME_TYPE_CLASSIC_MODE: "Classic Mode",
    GAME_TYPE_POUNDAMONIUM_OUTBREAK: "Poundamonium Outbreak",
    GAME_TYPE_POUNDAMONIUM_OUTBREAK_HARD: "Poundamonium Outbreak Hard",
    GAME_TYPE_POUNDAMONIUM_OUTBREAK_CLASSIC: "Poundamonium Outbreak Classic",
    GAME_TYPE_LEAGUE_OF_ZEDS: "League of ZEDs",
    GAME_TYPE_THE_HUSK_FLOOR: "The Husk Floor",
    GAME_TYPE_REALISM_OBJECTIVE_MOD: "Realism Objective Mod",
    GAME_TYPE_BOOM_WEEKLY_OUTBREAK_STANDALONE: "Boom",
    GAME_TYPE_BOOM_WEEKLY_OUTBREAK_STANDALONE_V2: "Boom V2",
    GAME_TYPE_BOBBLE_ZEDS_WEEKLY_OUTBREAK_STANDALONE: "BobbleZed",
    GAME_TYPE_BOBBLE_ZEDS_WEEKLY_OUTBREAK_STANDALONE_V2: "BobbleZed V2",
    GAME_TYPE_ZED_TIME_WEEKLY_OUTBREAK_STANDALONE: "ZedTime",
    GAME_TYPE_ZED_TIME_WEEKLY_OUTBREAK_STANDALONE_V2: "Zed Time V2",
    GAME_TYPE_TINY_TERROR_WEEKLY_OUTBREAK_STANDALONE: "Tiny Terror",
    GAME_TYPE_TINY_TERROR_WEEKLY_OUTBREAK_STANDALONE_V2: "Tiny Terror V2",
    GAME_TYPE_CRANIUM_CRACKER_WEEKLY_OUTBREAK_STANDALONE: "Cranium Cracker",
    GAME_TYPE_CRANIUM_CRACKER_WEEKLY_OUTBREAK_STANDALONE_V2: "Cranium Cracker V2",
    GAME_TYPE_DUMMY_MOD: "Dummy Mod",
    GAME_TYPE_CONTROLLED_DIFFICULTY_BLACKOUT: "Controlled Difficulty Blackout Edition",
    GAME_TYPE_ELITE_VERSUS: "Elite Versus",
    GAME_TYPE_CONTROLLED_DIFFICULTY: "Controlled Difficulty",
    GAME_TYPE_ABOMINATIONS_MINIBOSSES_SPAWN: "Mini Bosses"
}

GAME_MAP_TITLE_UNKNOWN = "KF-Default"

USER_TYPE_NONE = 0  # Enumerated ^2s for bitwise ops
USER_TYPE_ADMIN = 1
USER_TYPE_SPECTATOR = 2
USER_TYPE_INTERNAL = 4

ServerUpdateData = namedtuple(
    'ServerUpdateData', [
        # Most of these are used for new match detection and initialization
        'map_title', 'map_name', 'length', 'difficulty', 'game_type', 'wave',
        'capacity'
    ]
)

MatchUpdateData = namedtuple(
    'MatchUpdateData', [
        'trader_open', 'zeds_total', 'zeds_dead', 'wave'
    ]
)

PlayerUpdateData = namedtuple(
    'PlayerUpdateData', [
        'username', 'perk', 'kills', 'health', 'dosh', 'ping'
    ]
)

PlayerIdentityData = namedtuple('PlayerIdentityData', [
    'ip', 'country', 'country_code', 'steam_id', 'network_id', 'player_key'
])
