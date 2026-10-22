# Portable USB development — Orange Pi Zero 2W + Windows

**Verified October 13, 2026.** Direct USB networking works from a Windows laptop to an Orange Pi Zero 2W running Armbian, using ordinary SSH and SCP; VS Code Remote-SSH also connected during early experiments but is **no longer recommended** on this 1GB device. We tested SSH over USB, reboot persistence on the Orange Pi, and continued terminal access after disabling the Orange Pi's Wi-Fi.

This is a **network-over-USB** connection, not USB mass-storage flashing. Edit in **local Windows VS Code**, transfer with SCP, and run via terminal SSH; there is no need to remove the microSD card for routine updates.

## What worked

- Orange Pi Zero 2W running Armbian (observed kernel `6.18.55-current-sunxi64`)
- Gadget-capable **USB0** (the USB-C port previously assumed to be power-only) connected to Windows laptop using a confirmed data cable
- Separate USB-C **USB1** connected to the USB hub with Arduino UNO R3. This arrangement was observed working while laptop USB-SSH was connected.
- Linux USB gadget module: `g_ether`
- Orange Pi USB network interface: `usb0`, static address `192.168.7.2/24`
- Windows RNDIS network adapter: **Ethernet 6** on the test laptop, static address `192.168.7.1/24`
- SSH login: `ssh <your-orange-pi-username>@192.168.7.2` (actual test username: `mayok1921`)
- VS Code **Remote - SSH** connected to `192.168.7.2` during initial experiments; **use local VS Code + SCP/SSH instead** to save Orange Pi memory
- Wi-Fi on Orange Pi disabled for test: `sudo nmcli radio wifi off`; remote terminal still responded.

**Important:** USB0/USB1 are hardware functions, not interchangeable labels. Confirm the board's printed labeling and authoritative pin/port diagram when replicating this on a different board revision. During investigation, connecting the Windows cable to the other port led to `not attached` and no detected Windows device. Swapping the USB-C port assignments resolved USB enumeration.

## 1. Get the USB gadget to enumerate on Linux

During initial setup, preserve a *separate recovery access path* (working Wi-Fi SSH or a display and keyboard). The commands below change live state only; they do not by themselves make the IP address persistent.

```bash
ls /sys/class/udc
# Observed: musb-hdrc.4.auto

sudo modprobe g_ether
sudo ip link set usb0 up
sudo ip addr replace 192.168.7.2/24 dev usb0
cat /sys/class/udc/musb-hdrc.4.auto/state
```

With the cable connected to the **correct USB0 port**, `state` changed to **`configured`**, replacing `not attached`.

Additional verification:

```bash
ip addr show usb0
ip link show usb0
```

A `usb0` interface alone does **not** prove the physical USB link is connected: when the wrong port was used, `usb0` existed but showed `NO-CARRIER`, the UDC remained `not attached`, and `current_speed` read `UNKNOWN`.

## 2. Fix the Windows RNDIS driver binding (one-time per Windows computer)

When the correct USB port was used, Windows enumerated Linux's USB gadget at:

```text
USB\VID_0525&PID_A4A2
```

But Windows initially matched it as **USB Serial Device (COM7)** under Ports, not a network adapter. Installing the built-in `C:\Windows\INF\netrndis.inf` with `pnputil` **only registered the package** and did not fix the binding.

A matching **RNDIS.inf** and **rndis.cat** package was obtained from the **Microsoft Update Catalog** and extracted to a local directory. For additional laptops, choose a verified, appropriately signed driver package compatible with that Windows version/architecture and hardware ID. Do not download unverified third-party driver bundles, bypass driver signature checks, or force unrelated Arduino/serial drivers.

Microsoft Update Catalog search:
https://www.catalog.update.microsoft.com/Search.aspx?q=usb%5Cvid_0525%26pid_a4a2

In an elevated Windows PowerShell, after placing the matching extracted driver in `Downloads\RNDIS_Driver`:

```powershell
pnputil /add-driver "$env:USERPROFILE\Downloads\RNDIS_Driver\rndis.inf" /install
```

**Verified result:** `Driver package installed on device: USB\VID_0525&PID_A4A2\...`, published name `oem156.inf` on the test laptop. `oem156.inf` is a machine-specific name; don't hard-code it.

Then run:

```powershell
Get-NetAdapter
```

**Verified result:** `Ethernet 6` appeared as `USB Ethernet/RNDIS Gadget`, status **Up**. Other computers may use a different adapter name or interface number.

If the device still appears as a COM port, driver registration alone was insufficient: check whether `pnputil` explicitly states **installed on device**. Avoid changing drivers for unrelated COM ports.

## 3. Assign static IP addresses

On the Orange Pi:

```bash
sudo ip link set usb0 up
sudo ip addr replace 192.168.7.2/24 dev usb0
```

In **Administrator PowerShell** on Windows, substituting the adapter name from `Get-NetAdapter`:

```powershell
New-NetIPAddress -InterfaceAlias "Ethernet 6" -IPAddress 192.168.7.1 -PrefixLength 24
ping 192.168.7.2
ssh mayok1921@192.168.7.2
```

**Verified:** 4/4 successful pings with less than 1 ms reported; SSH login succeeded.

No gateway or DNS server is necessary on this point-to-point USB subnet. Keep the computer's regular Wi-Fi if desired; the Orange Pi doesn't need Wi-Fi for this connection.

**Windows persistence not yet verified across a Windows reboot or on a second laptop.** An observed Windows command returned entries for ActiveStore and PersistentStore; a fully clean-reboot check of the Windows adapter is still required.

## 4. Make the Orange Pi USB connection start automatically

One-time setup on Orange Pi:

```bash
echo g_ether | sudo tee /etc/modules-load.d/robotarm-usb.conf
```

Create `/etc/systemd/system/robotarm-usb.service` with the following content (also stored in this repository at [scripts/robotarm-usb.service](../scripts/robotarm-usb.service)):

```ini
[Unit]
Description=Robot Arm USB Network
After=systemd-modules-load.service
Requires=sys-subsystem-net-devices-usb0.device
After=sys-subsystem-net-devices-usb0.device

[Service]
Type=oneshot
ExecStart=/usr/sbin/ip link set usb0 up
ExecStart=/usr/sbin/ip addr replace 192.168.7.2/24 dev usb0
RemainAfterExit=yes

[Install]
WantedBy=multi-user.target
```

Enable it:

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now robotarm-usb.service
systemctl is-active robotarm-usb.service
```

**Verified:** `active`. The Orange Pi was rebooted; direct USB SSH reconnected afterward.

On the Orange Pi, `nmcli device status` shows `usb0` as **unmanaged**; this is expected because the interface is configured with a systemd service, not NetworkManager.

### Startup caveats

- The service uses `/usr/sbin/ip` as observed in the setup. Confirm `command -v ip` if using a different distribution.
- It depends on `g_ether` producing `usb0` and on `usb0` existing by the time systemd starts the service. `systemctl status robotarm-usb.service` and `journalctl -u robotarm-usb.service -b` are the first checks if a future boot fails.
- Wi-Fi radio state may be restored or changed by future updates/reboots; the proven test was USB SSH after disabling Orange Pi Wi-Fi, not a guarantee about every future network setting.
- Keep a recovery method until the arrangement works across multiple complete power cycles.

## 5. Use VS Code without Orange Pi Wi-Fi

On Windows, install VS Code and its **Remote - SSH** extension.

1. Connect the Windows USB data cable to Orange Pi USB0 and ensure the board is powered according to its hardware requirements.
2. Confirm the USB RNDIS adapter is present and has `192.168.7.1/24`.
3. VS Code → Command Palette → **Remote-SSH: Connect to Host** → `ssh mayok1921@192.168.7.2`.
4. If prompted for remote platform, choose **Linux**.
5. Open `/home/mayok1921/robotic_arm` and edit/run Python directly on the Orange Pi.

Do **not** distribute the original SSH password. For other contributors, create individual authorized SSH accounts/keys and document access provisioning separately.

**Verified offline network test:** `sudo nmcli radio wifi off` made `wlan0` unavailable while the USB VS Code terminal continued responding to `hostname` (`orangepizero2w`). VS Code Remote-SSH features may still attempt internet access for initial extension/server installation on a new laptop; prepare/install those components in advance when working fully offline.

## 6. Returning to robotic arm operation

- Current hardware setup permits **USB0 → laptop** and **USB1 → USB hub → Arduino** simultaneously.
- Arduino UNO R3 appeared as `/dev/ttyACM0` and controlled one unloaded SG90.
- Xbox controller communicates through Bluetooth; see [servo demo guide](servo_demo_guide.md).
- No laptop is required to run an already-installed Python program manually on the Orange Pi, but **automatic startup of the robotic-arm controller itself has not been configured or verified**.

## Troubleshooting reference

| Symptom | What actually mattered |
| --- | --- |
| `g_ether ready` but `usb0 NO-CARRIER`, UDC `not attached` | Gadget module loaded, but physical host connection was not established. Correct USB0 port assignment was crucial in our test. |
| UDC `configured` but Windows has no network adapter | Check Device Manager *and* hardware IDs. Windows had misclassified `VID_0525&PID_A4A2` as `USB Serial Device (COM7)`. |
| `netrndis.inf` package added but COM7 remains | Package registered, but not assigned. The matching catalog RNDIS driver package resolved this on our Windows installation. |
| `Get-NetAdapter` shows USB Ethernet/RNDIS Gadget Up but SSH fails | Check both static IPs, ping, SSH service, and local firewall. |
| USB SSH works manually but fails after reboot | Check module-loading file, systemd service and `ip addr show usb0`. |

## Outstanding validation

- Confirm the Windows USB adapter address survives a **Windows laptop reboot**.
- Confirm a full Orange Pi **power-off/power-on** recovery without Wi-Fi.
- Repeat onboarding with a second developer's laptop using its own SSH credentials.
- Test prolonged stability when Xbox Bluetooth + Arduino USB + laptop USB are active simultaneously.
- Establish a secure and documented initial provisioning/recovery method for future maintainers.

## October 21, 2026 — Repeat connection failure: Windows lost the expected USB adapter IPv4 address

**Observed symptoms:** Windows VS Code PowerShell `ssh mayok1921@192.168.7.2` initially timed out. The Orange Pi showed LED activity, but that alone did not confirm networking. Windows initially did not show the expected active USB network adapter; after the correct USB cable/port arrangement was restored, Windows detected **`Ethernet 7` — `USB Ethernet/RNDIS Gadget #2` — `Up`**. The name and number differed from the earlier `Ethernet 6` setup.

**Actual network fault observed:** `Get-NetIPAddress -InterfaceAlias "Ethernet 7" -AddressFamily IPv4` returned `169.254.69.180/16` (Windows link-local autoconfiguration), not the intended `192.168.7.1/24`. The Orange Pi's static address was still `192.168.7.2/24`, so the host and device were on different subnets. The reason Windows no longer had the expected IPv4 setting is **not proven**; the new adapter instance/alias is one possibility.

**Successful fix (Windows, PowerShell as Administrator):**

```powershell
Get-NetAdapter
Get-NetIPAddress -InterfaceAlias "Ethernet 7" -AddressFamily IPv4
New-NetIPAddress -InterfaceAlias "Ethernet 7" -IPAddress 192.168.7.1 -PrefixLength 24
ping 192.168.7.2
ssh mayok1921@192.168.7.2
```

Replace `Ethernet 7` with the **currently active RNDIS adapter name** from `Get-NetAdapter`; do not hard-code `Ethernet 6` or `Ethernet 7` across Windows instances. Before running `New-NetIPAddress`, check whether the correct address is already present to avoid duplicate-address errors. On this point-to-point USB interface no default gateway or DNS is required. Only change the intended USB gadget adapter, not Wi-Fi or the laptop's other Ethernet interfaces.

**Verified after recovery:**

- Windows `Ethernet 7` showed `USB Ethernet/RNDIS Gadget #2`, status `Up`.
- `Get-NetIPAddress` showed `192.168.7.1`, `/24`, `PrefixOrigin: Manual`, `AddressState: Preferred`.
- Ordinary terminal SSH reached the Orange Pi successfully.
- On the Orange Pi, `ip -4 addr show usb0` showed `usb0` UP with `inet 192.168.7.2/24` and `valid_lft forever`.
- During the initial address assignment Windows showed both ActiveStore and PersistentStore entries, but **persistence after a Windows restart was not tested** in this recovery.

**Diagnosis rule:**

1. If the RNDIS adapter is **absent**, first check the USB0 gadget port/cable and the RNDIS driver binding; see Sections 1–2 above. Do **not** assume every SSH timeout is an IP problem.
2. If the RNDIS adapter is **Up** but Windows has a `169.254.x.x` address, inspect/restore its expected `192.168.7.1/24` static address.
3. If the Windows address is already correct but SSH still fails, confirm `192.168.7.2/24` on Orange Pi `usb0`, check ping/SSH service, and retain a separate recovery access method.

**Remaining check:** unplug/reconnect USB and reboot Windows to verify the manual adapter address stays assigned to the correct RNDIS instance. The cause of the interface renaming remains unresolved.
