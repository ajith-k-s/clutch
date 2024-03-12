document.addEventListener('DOMContentLoaded', function () {
   var table = document.querySelector('.table-datatable');

   // Initialize the table as a DataTable
   var dataTable = initDataTable(table);

   // Event listener for search input
   var searchInput = document.getElementById('searchdata');
   searchInput.addEventListener('input', function () {
      var searchTerm = searchInput.value.toLowerCase();
      filterTable(searchTerm);
   });

   // Add Tailwind CSS classes to the table headers for sorting
   var headers = document.querySelectorAll('.table-datatable th');
   headers.forEach(function (header, index) {
      header.classList.add('cursor-pointer', 'hover:text-blue-600', 'bg-primary-content');

      // Event listener for column header click (sorting)
      header.addEventListener('click', function () {
         sortTable(table, index);

         // Remove existing chevron icons
         removeChevronIcons();

         // Add chevron icon to the clicked heading based on sorting order
         addChevronIcon(header);
      });
   });

   function initDataTable(table) {
      var headers = Array.from(table.querySelectorAll('th')).map(th => th.textContent);

      return {
         destroy: function () {
            // Your cleanup code here
         }
         // Additional DataTable functionalities can be added here
      };
   }

   function filterTable(searchTerm) {
      var rows = Array.from(table.querySelectorAll('tbody tr'));

      rows.forEach(function (row) {
         var rowText = row.textContent.toLowerCase();
         var isVisible = rowText.includes(searchTerm);
         row.style.display = isVisible ? '' : 'none';
      });
   }

   function sortTable(table, columnIndex) {
      var rows = Array.from(table.querySelectorAll('tbody tr'));

      var sortOrder = event.target.dataset.sortOrder || 'asc';

      // Remove data-sort-order from all headers
      headers.forEach(function (header) {
         delete header.dataset.sortOrder;
      });

      // Set data-sort-order for the clicked header
      event.target.dataset.sortOrder = sortOrder === 'asc' ? 'desc' : 'asc';

      rows.sort(function (a, b) {
         var aValue = a.children[columnIndex].textContent.trim();
         var bValue = b.children[columnIndex].textContent.trim();

         if (!isNaN(aValue) && !isNaN(bValue)) {
            return sortOrder === 'asc' ? aValue - bValue : bValue - aValue;
         } else {
            return sortOrder === 'asc' ? aValue.localeCompare(bValue) : bValue.localeCompare(aValue);
         }
      });

      table.querySelector('tbody').innerHTML = '';

      rows.forEach(function (row) {
         table.querySelector('tbody').appendChild(row);
      });
   }

   function removeChevronIcons() {
      var existingChevrons = document.querySelectorAll('.chevron-icon');
      existingChevrons.forEach(function (icon) {
         icon.remove();
      });
   }

   function addChevronIcon(header) {
      var sortOrder = header.dataset.sortOrder || 'asc';
      var chevronUp = createChevronIcon('M18 15l-6-6-6 6');
      var chevronDown = createChevronIcon('M6 9l6 6 6-6');

      if (sortOrder === 'asc') {
         header.appendChild(chevronUp);
      } else {
         header.appendChild(chevronDown);
      }
   }

   function createChevronIcon(pathData) {
      var svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
      svg.setAttribute('xmlns', 'http://www.w3.org/2000/svg');
      svg.setAttribute('class', 'size-6 chevron-icon');
      svg.setAttribute('viewBox', '0 0 24 24');
      svg.setAttribute('fill', 'none');
      svg.setAttribute('stroke', 'currentColor');
      svg.setAttribute('stroke-width', '2');
      svg.setAttribute('stroke-linecap', 'round');
      svg.setAttribute('stroke-linejoin', 'round');

      var path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
      path.setAttribute('d', pathData);

      svg.appendChild(path);
      return svg;
   }
});
