# The Implementations of Improved Signal Leakage Attacks 

Run attacks against DXL [DXL12]:
- `make`
- `python3 imp-dxl-pv.py`
- for comparing with the attack [BSV21], run `python3 compare-dxl.py`

Run attacks against DBS-KE [DBS19]:
- `make CFLAGS="-DVERS=19 -DN=512 -DSTDDEV=41915"`
- run `python3 imp-dbs-ke-pv.py 512`
- for comparing with the attack [BSV21], run `python3 compare-dbs-ke.py`

Run an attack against LBA-PAKE [DBK21]:
- `make CFLAGS="-DVERS=20"`
- run `python3 imp-lbapake-pv.py`



## Bibliography
[DXL12] Ding, J., Xie, X., Lin, X.: A Simple Provably Secure Key Exchange Scheme Based
on the Learning with Errors Problem. Cryptology ePrint Archive, Report 2019/688
(2012)


[DBS19] Ding, J., Branco, P., Schmitt, K.: Key Exchange and Authenticated Key Exchange
with Reusable Keys Based on RLWE Assumption. Cryptology ePrint Archive,
Report 2019/665 (2019)

[BSV21] Bindel, N., Stebila, D., Veitch, S.: Improved attacks against key reuse in learning
with errors key exchange. In: LATINCRYPT 2021. LNCS, Springer (2021)

[DBK21] V. Dabra, A. Bala and S. Kumari, "LBA-PAKE: Lattice-Based Anonymous Password Authenticated Key Exchange for Mobile Devices," in IEEE Systems Journal, vol. 15, no. 4, pp. 5067-5077, Dec. 2021
