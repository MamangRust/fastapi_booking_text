from fastapi import APIRouter, HTTPException, Depends
from dto.booking import Booking
from middleware.auth import get_current_user
from repository.booking_repository import TextBookingsRepository
from service.booking_service import BookingsService


text_bookings_repository = TextBookingsRepository("bookings.txt")
bookings_service = BookingsService(text_bookings_repository)

booking_router = APIRouter(prefix="/booking", tags=["Booking"])


@booking_router.post("/create")
def create_booking(booking: Booking, current_user=Depends(get_current_user)):
    bookings_service.create_booking(
        booking.tgl_pinjam,
        booking.user_id,
        booking.tgl_kembali,
        booking.tgl_pengembalian,
        booking.status,
        booking.total_denda,
    )
    return {"message": "Booking created successfully"}


@booking_router.get("/")
def get_all_bookings(current_user=Depends(get_current_user)):
    return bookings_service.get_all_bookings()


@booking_router.put("/update/{booking_id}")
def update_booking(
    booking_id: int, booking: Booking, current_user=Depends(get_current_user)
):
    updated = bookings_service.update_bookings(
        booking_id,
        booking.tgl_pinjam,
        booking.user_id,
        booking.tgl_kembali,
        booking.tgl_pengembalian,
        booking.status,
        booking.total_denda,
    )
    if not updated:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": f"Booking with ID {booking_id} updated successfully"}


@booking_router.delete("/{booking_id}")
def delete_booking(booking_id: int, current_user=Depends(get_current_user)):
    deleted = bookings_service.delete_booking(booking_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="Booking not found")
    return {"message": f"Booking with ID {booking_id} deleted successfully"}
