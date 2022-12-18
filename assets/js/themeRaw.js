(function() {
  "use strict"; // Start of use strict
  var sidebar = document.querySelector('.sidebar');
  var sidebarToggles = document.querySelectorAll('#sidebarToggle, #sidebarToggleTop');
  if (sidebar) {
    var collapseEl = sidebar.querySelector('.collapse');
    var collapseElementList = [].slice.call(document.querySelectorAll('.sidebar .collapse'))
    var sidebarCollapseList = collapseElementList.map(function (collapseEl) {
      return new bootstrap.Collapse(collapseEl, { toggle: false });
    });

    for (var toggle of sidebarToggles) {

      // Toggle the side navigation
      toggle.addEventListener('click', function(e) {
        document.body.classList.toggle('sidebar-toggled');
        sidebar.classList.toggle('toggled');

        if (sidebar.classList.contains('toggled')) {
          for (var bsCollapse of sidebarCollapseList) {
            bsCollapse.hide();
          }
        };
      });
    }

    // Close any open menu accordions when window is resized below 768px
    window.addEventListener('resize', function() {
      var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);
        
      if (vw < 768) {
        for (var bsCollapse of sidebarCollapseList) {
          bsCollapse.hide();
        }
      };
    });
  }

  // Prevent the content wrapper from scrolling when the fixed side navigation hovered over
  
  var fixedNaigation = document.querySelector('body.fixed-nav .sidebar');
  
  if (fixedNaigation) {
    fixedNaigation.on('mousewheel DOMMouseScroll wheel', function(e) {
      var vw = Math.max(document.documentElement.clientWidth || 0, window.innerWidth || 0);

      if (vw > 768) {
        var e0 = e.originalEvent,
          delta = e0.wheelDelta || -e0.detail;
        this.scrollTop += (delta < 0 ? 1 : -1) * 30;
        e.preventDefault();
      }
    });
  }

  var scrollToTop = document.querySelector('.scroll-to-top');
  
  if (scrollToTop) {
    
    // Scroll to top button appear
    window.addEventListener('scroll', function() {
      var scrollDistance = window.pageYOffset;

      //check if user is scrolling up
      if (scrollDistance > 100) {
        scrollToTop.style.display = 'block';
      } else {
        scrollToTop.style.display = 'none';
      }
    });
  }
    
  sidebarToggles[1].click()
    

})(); // End of use strict

function fallbackCopyTextToClipboard(text) {
  var textArea = document.createElement("textarea");
  textArea.value = text;
  
  // Avoid scrolling to bottom
  textArea.style.top = "0";
  textArea.style.left = "0";
  textArea.style.position = "fixed";

  document.body.appendChild(textArea);
  textArea.focus();
  textArea.select();

  try {
    var successful = document.execCommand('copy');
    var msg = successful ? 'successful' : 'unsuccessful';
    console.log('Fallback: Copying text command was ' + msg);
  } catch (err) {
    console.error('Fallback: Oops, unable to copy', err);
  }

  document.body.removeChild(textArea);
}
function copyTextToClipboard(text) {
  if (!navigator.clipboard) {
    fallbackCopyTextToClipboard(text);
    return;
  }
  navigator.clipboard.writeText(text).then(function() {
  }, function(err) {
  });
}
function myFunction() {
    // alert("Key is in clipboard Now!!");
    // After 3 seconds, remove the show class from DIV
    var jobValue = document.getElementsByName("txtQr")[0].value;
    alert(jobValue);
	copyTextToClipboard(jobValue);


  }

function search() {
  // Declare variables
  var input, filter, table, tr, td, i, txtValue;
  input = document.getElementById("searchInput");
  filter = input.value.toUpperCase();
  table = document.getElementById("dataTable");
  tr = table.getElementsByTagName("tr");

  // Loop through all table rows, and hide those who don't match the search query
  for (i = 0; i < tr.length; i++) {
    td = tr[i].getElementsByTagName("td")[0];
    if (td) {
      txtValue = td.textContent || td.innerText;
      if (txtValue.toUpperCase().indexOf(filter) > -1) {
        tr[i].style.display = "";
      } else {
        tr[i].style.display = "none";
      }
    }
  }
}


function check(id){
    // var a = document.getElementsByName("bt11")[0].style;
    // alert(a);
//         if (document.getElementsBy("bt1")[0].name == "bt11"){
    
    // if (id == '1'){
    // document.getElementById('inbound').value = '1';
    // document.getElementById('bt1').style.background = 'rgb(78,115, 223)';
    // document.getElementById('bt1').style.color = 'rgb(255,255, 255)';
    // document.getElementById('bt2').style.background = 'rgb(234,234,234)';
    // document.getElementById('bt2').style.color = 'rgb(72,65,65)';
    // document.getElementById('bt3').style.background = 'rgb(234,234,234)';
    // document.getElementById('bt3').style.color = 'rgb(72,65,65)';
    // }
    // if (id == '2'){
    // document.getElementById('inbound').value = '2';
    // document.getElementById('bt2').style.background = 'rgb(78,115, 223)';
    // document.getElementById('bt2').style.color = 'rgb(255,255, 255)';
    // document.getElementById('bt1').style.background = 'rgb(234,234,234)';
    // document.getElementById('bt1').style.color = 'rgb(72,65,65)';
    // }
    //$

}
