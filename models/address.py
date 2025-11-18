# This is just a template that we can follow for Location schema and microservice
from __future__ import annotations

from typing import Optional
from uuid import UUID, uuid4
from datetime import datetime
from pydantic import BaseModel, Field


class AddressBase(BaseModel):
    id: UUID = Field(
        default_factory=uuid4,
        description="Persistent Address ID (server-generated).",
        json_schema_extra={"example": "550e8400-e29b-41d4-a716-446655440000"},
    )
    name: str = Field(
        None,
        description="Name associated with the address (e.g., 'Bob's House').",
        json_schema_extra={"example": "Bob's House"},
    )
    street: str = Field(
        ...,
        description="Street address and number.",
        json_schema_extra={"example": "123 Main St"},
    )
    unit: Optional[str] = Field(
        None,
        description="Apartment, suite, unit, building, floor, etc.",
        json_schema_extra={"example": "Apt 4B"},
    )
    city: str = Field(
        ...,
        description="City or locality.",
        json_schema_extra={"example": "New York"},
    )
    state: Optional[str] = Field(
        None,
        description="State/region code if applicable.",
        json_schema_extra={"example": "NY"},
    )
    postal_code: Optional[str] = Field(
        None,
        description="Postal or ZIP code.",
        json_schema_extra={"example": "10001"},
    )
    country: str = Field(
        ...,
        description="Country name or ISO label.",
        json_schema_extra={"example": "USA"},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Bob's House",
                    "street": "123 Main St",
                    "unit": "Apt 4B",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "USA",
                }
            ]
        }
    }


class AddressCreate(AddressBase):
    """Creation payload; ID is generated server-side but present in the base model."""
    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "11111111-1111-4111-8111-111111111111",
                    "name": "Bob's House",
                    "street": "221B Baker St",
                    "unit": None,
                    "city": "London",
                    "state": None,
                    "postal_code": "NW1 6XE",
                    "country": "UK",
                }
            ]
        }
    }


class AddressUpdate(BaseModel):
    """Partial update; address ID is taken from the path, not the body."""
    name: Optional[str] = Field(
        None, description="Name associated with the address.", json_schema_extra={"example": "Bob's House"}
    )
    street: Optional[str] = Field(
        None, description="Street address and number.", json_schema_extra={"example": "124 Main St"}
    )
    unit: Optional[str] = Field(
        None, description="Apartment, suite, unit, building, floor, etc.", json_schema_extra={"example": "Apt 5C"}
    )
    city: Optional[str] = Field(
        None, description="City or locality.", json_schema_extra={"example": "New York"}
    )
    state: Optional[str] = Field(
        None, description="State/region code if applicable.", json_schema_extra={"example": "NY"}
    )
    postal_code: Optional[str] = Field(
        None, description="Postal or ZIP code.", json_schema_extra={"example": "10002"}
    )
    country: Optional[str] = Field(
        None, description="Country name or ISO label.", json_schema_extra={"example": "USA"}
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "Bob's House",
                    "street": "124 Main St",
                    "unit": "Apt 5C",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10002",
                    "country": "USA",
                },
                {"city": "Brooklyn"},
            ]
        }
    }


class AddressRead(AddressBase):
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Creation timestamp (UTC).",
        json_schema_extra={"example": "2025-01-15T10:20:30Z"},
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp (UTC).",
        json_schema_extra={"example": "2025-01-16T12:00:00Z"},
    )
    links: Optional[list] = Field(
        None,
        description="Linked data / relative links for this resource (e.g. [{rel: 'self', href: '/addresses/{id}'}]).",
        json_schema_extra={"example": [
            {"rel": "self", "href": "/addresses/550e8400-e29b-41d4-a716-446655440000"},
            {"rel": "collection", "href": "/addresses"}
        ]},
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "550e8400-e29b-41d4-a716-446655440000",
                    "name": "Bob's House",
                    "street": "123 Main St",
                    "unit": "Apt 4B",
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10001",
                    "country": "USA",
                    "created_at": "2025-01-15T10:20:30Z",
                    "updated_at": "2025-01-16T12:00:00Z",
                    "links": [
                        {"rel": "self", "href": "/addresses/550e8400-e29b-41d4-a716-446655440000"},
                        {"rel": "collection", "href": "/addresses"}
                    ],
                }
            ]
        }
    }


class AddressDelete(BaseModel):
    """Delete an Address by ID"""
    id: UUID = Field(..., description="ID of the address to delete.", json_schema_extra={"example": "99999999-9999-4999-8999-999999999999"})
    name: str = Field(..., description="Name associated with the address.", json_schema_extra={"example": "Bob's House"})
    street: Optional[str] = Field(..., description="Street address and number.", json_schema_extra={"example": "124 Main St"})
    unit: Optional[str] = Field(..., description="Apartment, suite, unit, building, floor, etc.", json_schema_extra={"example": "Apt 5C"})
    city: Optional[str] = Field(..., description="City or locality.", json_schema_extra={"example": "New York"})
    state: Optional[str] = Field(..., description="State/region code if applicable.", json_schema_extra={"example": "NY"})
    postal_code: Optional[str] = Field(..., description="Postal or ZIP code.", json_schema_extra={"example": "10002"})
    country: Optional[str] = Field(..., description="Country name or ISO label.", json_schema_extra={"example": "USA"})

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "id": "99999999-9999-4999-8999-999999999999",
                    "name": "Bob's House",
                    "street": "124 Main St",
                    "unit": "Apt 5C", 
                    "city": "New York",
                    "state": "NY",
                    "postal_code": "10002",
                    "country": "USA",
                }
            ]
        }
    }


def address_to_feature(address: dict, lon: float = -73.961967, lat: float = 40.808040) -> dict:
    """
    Map an address dict to a GeoJSON Feature dict.
    Coordinates are fake unless provided since we are using thrid-party map api
    """
    return {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [lon, lat],
        },
        "properties": {
            "name": address.get("name"),
            "address": address.get("street"),
            "unit": address.get("unit"),
            "city": address.get("city"),
            "state": address.get("state"),
            "country": address.get("country"),
            "postalCode": address.get("postal_code"),
            "size": address.get("size", "5x5"),
            "pricePerDay": address.get("pricePerDay", "15"),
        }
    }


def addresses_to_features(addresses: list, lon: float = -73.961967, lat: float = 40.808040) -> list:
    """
    Map a list of address dicts to a list of GeoJSON Feature dicts.
    """
    return [address_to_feature(addr, lon, lat) for addr in addresses]
