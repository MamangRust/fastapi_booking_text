from datetime import datetime


class TextBookingsRepository:
    def __init__(self, file_path):
        self.file_path = file_path

    def create_booking(self, booking_info):
        with open(self.file_path, "a") as file:
            file.write(booking_info + "\n")

    # Read all bookings from the file
    def read_all_bookings(self):
        with open(self.file_path, "r") as file:
            return file.readlines()

    # Create a booking with detailed information
    def create_booking_with_details(
        self, tgl_pinjam, user_id, tgl_kembali, tgl_pengembalian, status, total_denda
    ):
        booking_info = f"TglPinjam: {tgl_pinjam}, UserID: {user_id}, TglKembali: {tgl_kembali}, TglPengembalian: {tgl_pengembalian}, Status: {status}, TotalDenda: {total_denda}"

        # Calculate penalty if the return date is later than the due date
        if tgl_pengembalian > tgl_kembali:
            time_difference = tgl_pengembalian - tgl_kembali
            hours_late = time_difference.total_seconds() // 3600
            denda = hours_late * 10000
            total_denda += denda
            booking_info += f", Denda: {denda}"

        self.create_booking(booking_info)

    # Update an existing booking with detailed information
    def update_booking_with_details(
        self,
        booking_id,
        tgl_pinjam=None,
        user_id=None,
        tgl_kembali=None,
        tgl_pengembalian=None,
        status=None,
        total_denda=None,
    ):
        bookings = self.read_all_bookings()
        if 0 <= booking_id < len(bookings):
            booking_info = bookings[booking_id].strip().split(", ")

            # Prepare updated information based on provided or existing data
            updated_info = {
                "TglPinjam": tgl_pinjam
                if tgl_pinjam
                else booking_info[0].split(": ")[1],
                "UserID": user_id if user_id else booking_info[1].split(": ")[1],
                "TglKembali": tgl_kembali
                if tgl_kembali
                else booking_info[2].split(": ")[1],
                "TglPengembalian": tgl_pengembalian
                if tgl_pengembalian
                else booking_info[3].split(": ")[1],
                "Status": status if status else booking_info[4].split(": ")[1],
                "TotalDenda": total_denda
                if total_denda
                else booking_info[5].split(": ")[1],
            }

            # Check for late return and update penalty and status
            if (
                tgl_pengembalian
                and tgl_kembali
                and datetime.strptime(tgl_pengembalian, "%Y-%m-%d")
                > datetime.strptime(updated_info["TglKembali"], "%Y-%m-%d")
            ):
                time_difference = datetime.strptime(
                    tgl_pengembalian, "%Y-%m-%d"
                ) - datetime.strptime(updated_info["TglKembali"], "%Y-%m-%d")
                hours_late = time_difference.total_seconds() // 3600
                denda = hours_late * 10000
                updated_info["TotalDenda"] = str(
                    int(updated_info["TotalDenda"]) + denda
                )
                updated_info["Status"] = "Late Return"

            # Construct updated booking information
            updated_booking_info = f"TglPinjam: {updated_info['TglPinjam']}, UserID: {updated_info['UserID']}, TglKembali: {updated_info['TglKembali']}, TglPengembalian: {updated_info['TglPengembalian']}, Status: {updated_info['Status']}, TotalDenda: {updated_info['TotalDenda']}\n"

            # Update the booking in the file
            bookings[booking_id] = updated_booking_info
            with open(self.file_path, "w") as file:
                file.writelines(bookings)
        else:
            print("Booking ID out of range.")

    # Delete a booking based on the provided booking_id
    def delete_booking(self, booking_id):
        bookings = self.read_all_bookings()

        if 0 <= booking_id < len(bookings):
            del bookings[booking_id]

            # Remove the deleted entry and clean the list
            updated_bookings = [booking for booking in bookings if booking.strip()]

            # Update the file after deleting the booking
            with open(self.file_path, "w") as file:
                file.writelines(updated_bookings)
        else:
            print("Booking ID out of range.")
