
% case/14
/* case(Color, Type, MotherboardCompatibility, Manufacturer, IncludesPowerSupply,
        Internal3_5inBays, External5_25inBays, External5_25inSlimBays,
        External5_25inSlimSlotLoadBays, Internal2_5inBays,
        Internal3_5inBays, Internal5_25inBays, FontPanelUSBPorts,
        PartNumber)
*/
:- consult(case).

% cpu_cooler/11
/* cpu_cooler(Manufacturer, Model, SupportedSockets, BearingType,
       MinFanRPM, MaxFanRPM, MinNoiseLevel, MaxNoiseLevel,
       LiquidCooled, RadiatorSize, PartNumber)
*/
:- consult(cpu_cooler).

% cpu/16
/* cpu(Manufacturer, Model, DataWidth, Cores, Socket,
       OperatingFrequency, TurboFrequency, SimultaneousMultithreading,
       IntegratedGraphics, IncludesCPUCooler, L1Cache, L2Cache,
       L3Cache, Lithography, ThermalDesignPower, PartNumber)
*/
:- consult(cpu).

% internal_hard_drive/11
/* internal_hard_drive(Manufacturer, Capacity, Interface, FormFactor, RPM,
        NANDFlashType, Cache, HybridSSDCache, GB_per_Dollar, 'Dollars_per_GB',
        Part Number)
*/
:- consult(internal_hard_drive).

% memory/14
/* memory(Manufacturer, DDR_Generation, Clock_Speed, Size, Number_of_Dimms,
        CAS_Latency, ECC, HeatSpreader, Registered, Timing,
        Voltage, Type, Dollars_per_GB, PartNumber)
*/
:- consult(memory).

% motherboard/28
/* motherboard('CPU Socket', 'Chipset', 'Color', 'CrossFire Support', 'Form Factor',
        'Half Mini-PCI-Express', 'Manufacturer', 'Maximum Supported Memory',
        'Memory Slots', 'Memory Type', 'Micro SATA 6 Gb/s', 'Mini-PCI-Express',
        'Mini-PCI-Express/mSATA', 'Onboard Ethernet',
        'Onboard USB 3.0 Header(s)', 'Onboard Video', 'PATA 100', 'Part Number',
        'RAID Support', 'SATA 3 Gb/s', 'SATA 6 Gb/s', 'SATA Express',
        'SLI Support', 'U.2', 'U.2 (SFF-8639)', 'eSATA 3Gb/s', 'eSATA 6Gb/s')
*/
:- consult(motherboard).

% power_supply/13
/* power_supply(Wattage, Efficiency, EfficiencyCertification, Modular,
        Manufacturer, Fanless, Output, Type, Color,
        PCIExpress_6plus2_PinConnectors, PCIExpress_6Pin_Connectors,
        'PCIExpress_8Pin_Connectors', 'PartNumber')
*/
:- consult(power_supply).

% video_card/27
/* video_card(Chipset, Manufacturer, MemorySize, MemoryType, CoreClock,
        BoostClock, Interface, Color, Length, Fan, TDP,
        SupportsFreesync, SupportsGSync, CrossFireSupport,
        SLISupport, VGAPorts, VHDCIPorts, DVIDDualLinkPorts, DVIDSingleLinkPorts,
        DVIIDualLinkPorts, SVideoPorts, HDMIPorts, MiniHDMIPorts, DisplayPortPorts,
        MiniDisplayPortPorts', VirtualLinkPorts, PartNumber
*/
:- consult(video_card).