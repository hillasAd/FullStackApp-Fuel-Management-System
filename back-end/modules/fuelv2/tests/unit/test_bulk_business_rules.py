import pytest
from modules.fuelv2.domain.entities import BulkStatus
from modules.fuel.domain.value_objects import  FuelAmount
from modules.fuel.domain.exceptions import InvalidFuelStateTransition, TankCapacityExceeded
from modules.fuelv2.domain.value_objects import BulkItemStatus
from modules.fuelv2.domain.entities import BulkFuelRequestItem


def test_should_raise_error_when_item_exceeds_tank_capacity(dummy_vehicle_entity):
    with pytest.raises(TankCapacityExceeded):
        BulkFuelRequestItem(id=None, vehicle=dummy_vehicle_entity, amount=FuelAmount(90))

def test_sync_status_to_cancelled_when_all_items_are_rejected(bulk_entity_factory):
    bulk = bulk_entity_factory(items_count=2)
    for item in bulk.items:
        item.status = BulkItemStatus.REJECTED
    bulk.sync_status()
    assert bulk.status == BulkStatus.CANCELLED

def test_prevent_adding_items_to_processed_bulk(bulk_entity_factory, dummy_vehicle_entity):
    bulk = bulk_entity_factory(status=BulkStatus.PROCESSED)
    with pytest.raises(InvalidFuelStateTransition):
        bulk.add_item(dummy_vehicle_entity, FuelAmount(10))
