class BookingsService:
    def __init__(self, repository):
        self.repository = repository

    # Create a booking entry with detailed information
    def create_booking(
        self, tgl_pinjam, user_id, tgl_kembali, tgl_pengembalian, status, total_denda
    ):
        self.repository.create_booking_with_details(
            tgl_pinjam, user_id, tgl_kembali, tgl_pengembalian, status, total_denda
        )

    # Retrieve all bookings from the repository
    def get_all_bookings(self):
        return self.repository.read_all_bookings()

    # Update a booking's information based on provided details
    def update_bookings(
        self,
        booking_id,
        tgl_pinjam=None,
        user_id=None,
        tgl_kembali=None,
        tgl_pengembalian=None,
        status=None,
        total_denda=None,
    ):
        return self.repository.update_booking_with_details(
            booking_id,
            tgl_pinjam,
            user_id,
            tgl_kembali,
            tgl_pengembalian,
            status,
            total_denda,
        )

    # Delete a booking entry using its ID
    def delete_booking(self, booking_id):
        return self.repository.delete_booking(booking_id)
