# to use this do 'python -m pip install pytest' in cmd
# run command:  pytest project/
import pytest
import xml.etree.ElementTree
import blueprintUtils
import weaponExport
from weaponExport import Weapon
import wikiWeaponTables


allColumnsSet =  set(wikiWeaponTables.allColumns)
# https://realpython.com/python-testing/#automated-vs-manual-testing
# https://realpython.com/pytest-python-testing/#marks-categorizing-tests

damageAbbr = weaponExport.damageAbbr
infiniteAbbr = weaponExport.infiniteAbbr
@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', '1'),
    ('LASER_BIO', ''),
    ('BEAM_REPAIR', '-2'), 
    ('LASER_CHAINGUN_DAMAGE', damageAbbr.format(1, 3, 0.5, 4)), # chain
    ('BEAM_ADAPT', infiniteAbbr.format(1, 0.75)), # infinite
    # TODO: systemless rooms
])
def testGetHullDamage(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint, allColumnsSet)
    assert weapon.getHullDamage() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', '1'),
    ('LASER_BIO', ''), # damage =  0
    ('BOMB_FIRE', ''), # sysDamage = 0
    ('MISSILES_4', '5'), # sysDamage with damage
    ('MISSILES_ENERGY', ''), # noSysDamage = true
    ('LASER_LIGHT_CHARGEGUN', ''), # <sysDamage>-1</sysDamage>
    ('BOMB_BREACH_1', '2'), # sysDamage, <damage>0</damage>
    ('BOMB_HEAL_SYSTEM', '-8'), # (-) sysDamage plus (-) damage
    ('LASER_CHAINGUN_DAMAGE', damageAbbr.format(1, 3, 0.5, 4)), # chain
    ('BEAM_ADAPT', infiniteAbbr.format(1, 0.75)), # infinite
])
def testGetSysDamage(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint, allColumnsSet)
    assert weapon.getSysDamage() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', '15'),
    ('ION_1', ''),
    ('BEAM_STUN', '30'), # only persDamage
    ('BEAM_BIO', f'60{weaponExport.icons["rad"]}'), # with "rad"
    ('LASER_CHAINGUN_DAMAGE', damageAbbr.format(15, 45, 7.5, 4)), # chain
    ('BEAM_ADAPT', infiniteAbbr.format(15, 11.25)), # infinite
])
def testGetCrewDamage(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint, allColumnsSet)
    assert weapon.getCrewDamage() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', ''),
    ('ION_1', '1'),
    ('SHOTGUN_ION', '1'), # damage separate from ion
    ('ION_PIERCE_CHAIN', damageAbbr.format(1, 5, 1, 4)), # chain
])
def testGetIonDamage(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint, allColumnsSet)
    assert weapon.getIonDamage() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('BEAM_1', ''),
    ('LASER_BURST_2', '2'),
     # missile cost
    ('MISSILES_FREE', '1'),
    ('MISSILES_1', '1/1{{Missile}}'),
    ('SLOTGUN_CHAOS', '12/3{{Missile}}'),
    # <projectiles><projectile>.count
    ('SHOTGUN_1', '2'),
    ('SHOTGUN_2', '3'),
    ('CLONE_CANNON_BABYORCHID', '20'),
    ('RUSTY_MISSILES_BURST', '2/1{{Missile}}'),
     # chargeLevels
    ('LASER_CHARGEGUN', '1-2'),
    ('SHOTGUN_CHARGE', '1-3'),
    # chargeLevel / missiles
    ('MISSILES_BURST', '1-3/1{{Missile}}'),
    # ammo chance (TODO)
    ('KERNEL_1', '2/1{{Missile}}'),
    # accuracy
    ('BOMB_1', '1/1{{Missile}} {{Accuracy|30}}'),
    ('LOOT_MATH_2', '1/2{{Missile}} {{Accuracy|30}}'),
])
def testGetShots(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getShots() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    # regular pierce
    ('LASER_BURST_1', ''),
    ('LASER_PIERCE', '1'),
    ('MODULAR_ION_BASE_PIERCE', '3'),
    # beam piercing
    ('BEAM_2', ''),
    ('BIG_ION_CHAOS', '11'),
    ('BEAM_PIERCE', '2'),
    ('BEAM_FIRE_PIERCE', '3'),
    # missile pierce
    ('MISSILES_1', '10'),
    # gaster_blaster
    ('GASTER_BLASTER', '')
])
def testGetPierce(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getPierce() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', ''),
    ('SHOTGUN_1', '42px'),
    ('RUSTY_LASER_BURST_2', '52px'),
    ('RUSTY_MISSILES_1', '52px')
])
def testGetRadius(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getRadius() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', ''),
    ('BEAM_1', '45px'),
    ('POWER_CORE', '')
])
def testGetLength(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getLength() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', '1'),
    ('LASER_CONSERVATIVE', '0'),
    ('BEAM_BATTERY', '<abbr title="Provides 2 power to the weapon to its right.">-2</abbr>'),
    ('POWER_CORE', '<abbr title="Provides 3 power to the weapon to its right.">-3</abbr>')
])
def testGetPower(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getPower() == expected

cooldownAbbr = weaponExport.cooldownAbbr
preemptAbbr = weaponExport.preemptAbbr
fireTimeAbbr = weaponExport.fireTimeAbbr
startChargedAbbr = weaponExport.startChargedAbbr

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', '9'),
    ('LASER_CHARGEGUN', '6.5'),
    ('CLONE_CANNON', ''),
    # Chain weapons (Cooldown boost)
    ('LASER_CHAINGUN', cooldownAbbr.format(15, 6, 3, 3)),
    ('LASER_CHARGE_CHAIN', cooldownAbbr.format(7.5, 3, 1.5, 3)),
    # Instant weapons
    ('ION_INSTANT', preemptAbbr.format(1)),
    ('LOOT_MATH_5', preemptAbbr.format(15)),
    # fireTime
    ('STRAWBERRY_CHAOS', f'40/{fireTimeAbbr.format(0.05)}'),
    # Chain weapons / fireTime
    ('GATLING_SYLVAN', f'{cooldownAbbr.format(20, 0, 20, 1)}/{fireTimeAbbr.format(0.2)}'),
    # startCharged / fireTime
    ('GATLING_ANCIENT', f'{startChargedAbbr}/{fireTimeAbbr.format(0.05)}')
])
def testGetCooldown(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getCooldown() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_HEAVY_PIERCE', ''),
    ('LASER_BURST_1', '10%')
])
def testGetFireChance(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getFireChance() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', ''),
    ('LASER_HEAVY_PIERCE', '40%')
])
def testGetStun(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getBreachChance() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', ''),
    ('LASER_HEAVY_PIERCE', '20% (3s)'),
    ('LASER_STUN', '100% (16s)')
])
def testGetStun(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getStun() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', '40 {{Scrap}}'),
    ('CRASH_LASER', '0 {{Scrap}}')
])
def testGetCost(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getCost() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    ('LASER_BURST_1', '0'),
    ('LASER_BURST_2', '3')
])
def testGetRarity(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getRarity() == expected

@pytest.mark.parametrize('blueprintName, expected', [
    # defaults
    ('LASER_BURST_1', weaponExport.defaultSpeeds['LASER']), # LASER
    ('LASER_CHAINGUN_2', weaponExport.defaultSpeeds['BURST']), # BURST
    ('MISSILES_PARTICLE', weaponExport.defaultSpeeds['MISSILES']), # MISSILES
    ('BEAM_PARTICLE', weaponExport.defaultSpeeds['BEAM']), # BEAM
    # normal
    ('ION_1', '30'),
    ('BOMB_1', ''),
    ('MODULE_ACCURACY', '')
])
def testGetSpeed(blueprintName, expected):
    blueprintPath = f'.//weaponBlueprint[@name="{blueprintName}"]'
    blueprint = blueprintUtils.getNormalBlueprint(blueprintPath)
    weapon = Weapon(blueprint)
    assert weapon.getSpeed() == expected
