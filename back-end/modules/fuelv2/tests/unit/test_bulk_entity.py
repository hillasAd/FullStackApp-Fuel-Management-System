import pytest
from modules.fuelv2.domain.entities import BulkStatus
from modules.fuelv2.domain.value_objects import BulkItemStatus

def test_bulk_status_should_remain_pending_if_no_items_altered(bulk_entity_factory):
    bulk = bulk_entity_factory(items_count=2)
    bulk.sync_status()
    assert bulk.status == BulkStatus.PENDING

def test_bulk_status_should_be_processed_if_at_least_one_item_is_approved(bulk_entity_factory):
    bulk = bulk_entity_factory(items_count=2)
    bulk.items[0].approve(admin_id=1)
    bulk.sync_status()
    assert bulk.status == BulkStatus.PROCESSED

def test_cancel_master_should_propagate_to_all_pending_items(bulk_entity_factory):
    bulk = bulk_entity_factory(items_count=2)
    bulk.cancel_master(reason="Cancelamento mestre")
    assert bulk.status == BulkStatus.CANCELLED
    assert bulk.items[0].status == BulkItemStatus.CANCELLED
    assert bulk.items[1].status == BulkItemStatus.CANCELLED
