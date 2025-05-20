document.addEventListener('DOMContentLoaded', () => {
    const machinesTableBody = document.getElementById('machines-data');
    const statusFilter = document.getElementById('status-filter');
    const inactivityFilter = document.getElementById('inactivity-filter');
    const machineIdDisplay = document.getElementById('machine-id');

    // Single Machine Demo JSON data with historical entries
    const demoData = [
        {
            "machine_id": "Machine128",
            "timestamp": 1747833600, // 2025-07-19 00:00:00
            "os": "Windows",
            "os_version": "11.0.22621",
            "disk_encrypted": true,
            "os_updates": "Up to date",
            "antivirus": "Antivirus: Microsoft Defender",
            "inactivity_sleep": "OK"
        },
        {
            "machine_id": "Machine128",
            "timestamp": 1747823600, // 2025-07-18 21:13:20
            "os": "Windows",
            "os_version": "11.0.22621",
            "disk_encrypted": true,
            "os_updates": "Up to date",
            "antivirus": "Antivirus: Microsoft Defender",
            "inactivity_sleep": "Too long (20 mins)" // Issue introduced
        },
        {
            "machine_id": "Machine128",
            "timestamp": 1747747200, // 2025-07-17 00:00:00
            "os": "Windows",
            "os_version": "11.0.22621",
            "disk_encrypted": true,
            "os_updates": "2 updates available", // Issue introduced
            "antivirus": "Antivirus: Microsoft Defender",
            "inactivity_sleep": "OK"
        },
        {
            "machine_id": "Machine128",
            "timestamp": 1747660800, // 2025-07-16 00:00:00
            "os": "Windows",
            "os_version": "11.0.22621",
            "disk_encrypted": false, // Issue introduced
            "os_updates": "Up to date",
            "antivirus": "Antivirus: Microsoft Defender",
            "inactivity_sleep": "OK"
        },
        {
            "machine_id": "Machine128",
            "timestamp": 1747574400, // 2025-07-15 00:00:00
            "os": "Windows",
            "os_version": "11.0.22621",
            "disk_encrypted": true,
            "os_updates": "Up to date",
            "antivirus": "Antivirus: Microsoft Defender",
            "inactivity_sleep": "OK"
        }
    ];

    function formatDate(timestamp) {
        const date = new Date(timestamp * 1000);
        return date.toLocaleString();
    }

    function getStatusClass(machine) {
        if (!machine.disk_encrypted || machine.os_updates.includes("available") || machine.inactivity_sleep.includes("Too long")) {
            return "issue";
        } else if (machine.disk_encrypted && !machine.os_updates.includes("available") && !machine.inactivity_sleep.includes("Too long")) {
            return "ok";
        } else {
            return "unknown";
        }
    }

    function renderTable(data) {
        machinesTableBody.innerHTML = ''; // Clear the table
        data.forEach(item => { // Iterate through the array of data
            const row = machinesTableBody.insertRow();
            row.classList.add(getStatusClass(item));

            const machineIdCell = row.insertCell();
            machineIdCell.textContent = item.machine_id;

            const osCell = row.insertCell();
            osCell.textContent = item.os;

            const diskEncryptedCell = row.insertCell();
            diskEncryptedCell.textContent = item.disk_encrypted ? "Yes" : "No";

            const osUpdatesCell = row.insertCell();
            osUpdatesCell.textContent = item.os_updates;

            const antivirusCell = row.insertCell();
            antivirusCell.textContent = item.antivirus;

            const inactivitySleepCell = row.insertCell();
            inactivitySleepCell.textContent = item.inactivity_sleep;

            const lastCheckinCell = row.insertCell();
            lastCheckinCell.textContent = formatDate(item.timestamp);
        });
    }

    function filterData() {
        const selectedStatus = statusFilter.value;
        const selectedInactivity = inactivityFilter.value;
        let filteredData = demoData; // Start with all the data

        if (selectedStatus) {
            filteredData = filteredData.filter(item => getStatusClass(item) === selectedStatus);
        }

        if (selectedInactivity) {
            filteredData = filteredData.filter(item => item.inactivity_sleep === selectedInactivity);
        }

        renderTable(filteredData);
    }

    if (machineIdDisplay) {
        machineIdDisplay.textContent = demoData[0].machine_id; // Display the machine ID
    }

    statusFilter.addEventListener('change', filterData);
    inactivityFilter.addEventListener('change', filterData); // Add listener for inactivity filter

    renderTable(demoData); // Initial rendering of all data
});