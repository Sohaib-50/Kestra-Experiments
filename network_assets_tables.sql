CREATE TABLE IF NOT EXISTS public.network_asset_scan
(
    id serial PRIMARY KEY,
    scan_args text,
    nmap_version text,
    scan_finished_timestamp timestamp WITHOUT TIME ZONE;
    scan_summary text,
    hosts_scanned integer,
    hosts_up integer,
    hosts_down integer,
    host_status text,
	requested_ip_address text,
    address text,
    address_type text,
    hostname text,
    raw_scan_info jsonb  
);

ALTER TABLE IF EXISTS public.network_asset_scan
    OWNER to kestra;

CREATE TABLE IF NOT EXISTS public.network_asset_scan_os_guesses
(
    id serial PRIMARY KEY,
    name text,
    accuracy integer,
    network_asset_scan_id integer REFERENCES public.network_asset_scan(id) ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public.network_asset_scan_os_guesses
    OWNER to kestra;

CREATE TABLE IF NOT EXISTS public.network_asset_scan_ports
(
    id serial PRIMARY KEY,
    number integer,
    protocol text,
    state text,
    service_name text,
    service_product text,
    service_version text,
    network_asset_scan_id integer REFERENCES public.network_asset_scan(id) ON DELETE CASCADE
);

ALTER TABLE IF EXISTS public.network_asset_scan_ports
    OWNER to kestra;

