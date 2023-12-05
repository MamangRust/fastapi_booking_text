from pydantic import BaseModel


class Booking(BaseModel):
    tgl_pinjam: str
    user_id: int
    tgl_kembali: str
    tgl_pengembalian: str
    status: str
    total_denda: int
