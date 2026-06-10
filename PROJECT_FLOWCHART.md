# SIAKTERNAK Project Flowchart

## Overview
This flowchart describes the full application flow for the `siakternak` project, including screen navigation, user actions, and database operations.

## Mermaid diagram
```mermaid
flowchart TD
    A[App Launch: main.py] --> B[Init DB: database.init_db()]
    B --> C[ScreenManager]

    subgraph Auth & Landing
        C --> D[LoginScreen]
        C --> E[LandingScreen]
        D -->|successful login| F[MainScreen]
        D -->|failed login| D
        D -->|back to portal| E
        E -->|login button| D
        E -->|order button| G[OrderFormScreen]
        G -->|submit order| H[OrderSuccessScreen]
        H -->|back to landing| E
        G -->|validate fields| G
        G -->|add order| DB_Pesanan[database.add_pesanan()]
    end

    subgraph Main App
        F --> I[Bottom Navigation Tabs]
        I --> J[BerandaScreen]
        I --> K[PembeliScreen]
        I --> L[DataScreen]
        I --> M[InventarisScreen]
        I --> N[KeuanganScreen]
        F --> O[Profile Menu]
        O -->|Ubah Password| DB_ChangePass[database.change_password()]
        O -->|Registrasi User Baru| DB_Register[database.register_user()]
        O -->|Daftar & Hapus User| DB_UserList[database.get_all_users()/delete_user()]
    end

    subgraph Beranda
        J -->|on_enter/trigger_loading| DB_Summary[database.get_summary()]
        DB_Summary --> J
        J -->|chart data| DB_Monthly[database.get_monthly_summary()]
        DB_Monthly --> J
        J -->|show details| Dialog_LabaRugi
    end

    subgraph Pembeli
        K -->|on_enter| DB_GetOrders[database.get_all_pesanan()]
        DB_GetOrders --> K
        K -->|approve/reject| DB_UpdateStatus[database.update_status_pesanan()]
        DB_UpdateStatus --> K
    end

    subgraph Data Management
        L -->|on_enter or tab switch| L
        L -->|pemasukan tab| DB_GetPemasukan[database.get_all_pemasukan()]
        L -->|pengeluaran tab| DB_GetPengeluaran[database.get_all_pengeluaran()]
        L --> DB_SavePemasukan[database.add_pemasukan()/update_pemasukan()/delete_pemasukan()]
        L --> DB_SavePengeluaran[database.add_pengeluaran()/update_pengeluaran()/delete_pengeluaran()]
        DB_SavePemasukan --> DB_SyncInv1[database.inventaris sync]
        DB_SavePengeluaran --> DB_SyncInv2[database.inventaris sync]
    end

    subgraph Inventaris
        M -->|on_enter| DB_InventorySummary[database.get_inventory_summary()]
        M -->|load table| DB_GetInventaris[database.get_all_inventaris()]
        M -->|manual add/edit/delete| DB_InventarisManual[database.add_inventaris_manual()/update_inventaris_manual()/delete_inventaris_manual()]
    end

    subgraph Keuangan & Accounting
        N -->|select module| P[Accounting Screens]
        P --> Q[Daftar Akun (COA)]
        P --> R[Jurnal Umum]
        P --> S[Buku Besar]
        P --> T[Neraca Saldo]
        P --> U[Laba Rugi]
    end

    subgraph Database
        DB_Pesanan --> V[pesanan table]
        DB_GetOrders --> V
        DB_UpdateStatus --> V
        DB_Summary --> W[pemasukan + pengeluaran tables]
        DB_Monthly --> W
        DB_GetPemasukan --> X[pemasukan table]
        DB_GetPengeluaran --> Y[pengeluaran table]
        DB_GetInventaris --> Z[inventaris table]
        DB_InventorySummary --> Z
        DB_SyncInv1 --> Z
        DB_SyncInv2 --> Z
        DB_InventarisManual --> Z
    end
``` 

## Key flows
- `main.py` starts the app and initializes the database.
- The first screen shown is `LoginScreen`.
- From `LoginScreen`, the user can log in or return to `LandingScreen`.
- `LandingScreen` supports product browsing and direct order placement.
- `OrderFormScreen` validates input, writes a new order to `pesanan` table, then shows `OrderSuccessScreen`.
- On successful login, `MainScreen` loads and shows a bottom navigation with five main modules.
- `BerandaScreen` renders dashboard data using `database.get_summary()` and `database.get_monthly_summary()`.
- `PembeliScreen` shows all buyer orders and allows accept/reject status updates.
- `DataScreen` manages financial records: income (`pemasukan`) and expenses (`pengeluaran`), with add/edit/delete operations.
- `InventarisScreen` displays inventory/stock summary and manual inventory adjustments.
- `KeuanganScreen` routes into accounting reports and ledgers (COA, Jurnal, Buku Besar, Neraca, Laba Rugi).
- The profile menu supports user management and password changes.

## Notes
- Income and expense changes automatically sync into `inventaris`.
- Inventory summary is used by `OrderFormScreen` to validate stock availability.
- `database.init_db()` also seeds default admin and sample data.
