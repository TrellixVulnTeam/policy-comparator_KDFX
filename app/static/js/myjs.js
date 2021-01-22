const ID_RE = /(-)_(-)/;

/**
 * Replace the template index of an element (-_-) with the
 * given index.
 */
function replaceTemplateIndex(value, index) {
    return value.replace(ID_RE, '$1'+index+'$2');
}

/**
 * Adjust the indices of form fields when removing items.
 */
function adjustIndices(removedIndex) {
    var $forms = $('.subform');

    $forms.each(function(i) {
        var $form = $(this);
        var index = parseInt($form.data('index'));
        var newIndex = index - 1;

        if (index < removedIndex) {
            // Skip
            return true;

        }

        // This will replace the original index with the new one
        // only if it is found in the format -num-, preventing
        // accidental replacing of fields that may have numbers
        // intheir names.
        var regex = new RegExp('(-)'+index+'(-)');
        var repVal = '$1'+newIndex+'$2';

        // Change ID in form itself
        $form.attr('id', $form.attr('id').replace(index, newIndex));
        $form.data('index', newIndex);

        // Change IDs in form fields
        $form.find('h4, label, input, select, textarea').each(function(j) {
            var $item = $(this);

            if ($item.is('label')) {
                // Update labels
                $item.attr('for', $item.attr('for').replace(regex, repVal));
                return;
            }
            if (document.getElementById('authors-_-form')){
                if ($item.is('h4')) {
                    // Update labels
                    var index = newIndex + 1
                    $item.text('Author '+index);
                    return;
                }
            } else if (document.getElementById('list-_-form')){
                if ($item.is('h4')) {
                    // Update labels
                    var index = newIndex + 1
                    $item.text('Policy-Target '+index);
                    return;
                }
            }
            

            // Update other fields
            $item.attr('id', $item.attr('id').replace(regex, repVal));
            $item.attr('name', $item.attr('name').replace(regex, repVal));
        });
    });
}

/**
 * Remove a form.
 */
function removeForm() {
    // If we're in an author form
    if (document.getElementById('authors-_-form')){
        var $removedForm = $(this).closest('.subform');
        var removedIndex = parseInt($removedForm.data('index'));
        $removedForm.remove();
        // Update indices
        adjustIndices(removedIndex);
        // Then checks if we're in a result form
    } else if (document.getElementById('list-_-form')){
        var $removedForm = $(this).closest('.subform');
        var removedIndex = parseInt($removedForm.data('index'));
        $removedForm.remove();
        // Update indices
        adjustIndices(removedIndex);
    }
}

// Function that clears the page from empty form row when loading page
function clear(){
    // Firstly checks if we are with an author form 
    if (document.getElementById('authors-_-form')){
        // Then checks if the first form is empty
        if (document.getElementById('authors-0-firstname').value === ''){
            var form = document.getElementById('authors-0-form')
            var removedIndex = parseInt(form.index);
            // Deletes it if empty
            form.remove();
            adjustIndices(removedIndex);
        }
        // Then checks if we're in a result form
    } else if (document.getElementById('list-_-form')){
        // Once again, if the first form is empty, it is deleted
        if (document.getElementById('list-0-policy').value === ''){
            var form = document.getElementById('list-0-form')
            var removedIndex = parseInt(form.index);
            form.remove();
            adjustIndices(removedIndex);
        }
    }
    
}


/**
 * Add a new form.
 */
function addForm() {
    if (document.getElementById('authors-_-form')){
        var $templateForm = $('#authors-_-form');
        if ($templateForm.length === 0) {
            console.log('[ERROR] Cannot find template');
            return;
        }

        // Get Last index
        var $lastForm = $('.subform').last();
        var newIndex = 0;
        if ($lastForm.length > 0) {
            newIndex = parseInt($lastForm.data('index')) + 1;
        } else {
            newIndex = 0
        }

        // Maximum of 20 subforms
        if (newIndex >= 20) {
            console.log('[WARNING] Reached maximum number of authors');
            return;
        }

        // Add elements
        var $newForm = $templateForm.clone();
        $newForm.attr('id', replaceTemplateIndex($newForm.attr('id'), newIndex));
        $newForm.data('index', newIndex);
        $newForm.find('h4, label, input, select, textarea').each(function(idx) {
            var $item = $(this);

            if ($item.is('label')) {
                // Update labels
                $item.attr('for', replaceTemplateIndex($item.attr('for'), newIndex));
                return;
            }
            if ($item.is('h4')) {
                // Update labels
                var index = newIndex + 1
                $item.text('Author '+index);
                return;
            }
            // Update other fields
            $item.attr('id', replaceTemplateIndex($item.attr('id'), newIndex));
            $item.attr('name', replaceTemplateIndex($item.attr('name'), newIndex));
        });
        // Append
        $('#subforms-container').append($newForm);
        $newForm.addClass('subform');
        $newForm.removeClass('is-hidden');
        $newForm.find('.removeBtn').click(removeForm);

       


    } else if (document.getElementById('list-_-form')){
        var $templateForm = $('#list-_-form');

        if ($templateForm.length === 0) {
            console.log('[ERROR] Cannot find template');
            return;
        }

        // Get Last index
        var $lastForm = $('.subform').last();

        var newIndex = 0;

        if ($lastForm.length > 0) {
            newIndex = parseInt($lastForm.data('index')) + 1;
        } else {
            newIndex = 0;
        }

        // Maximum of 20 subforms
        if (newIndex >= 20) {
            console.log('[WARNING] Reached maximum number of elements');
            return;
        }

        // Add elements
        var $newForm = $templateForm.clone();

        $newForm.attr('id', replaceTemplateIndex($newForm.attr('id'), newIndex));
        $newForm.data('index', newIndex);

        $newForm.find('h4, label, input, select, textarea').each(function(idx) {
            var $item = $(this);

            if ($item.is('label')) {
                // Update labels
                $item.attr('for', replaceTemplateIndex($item.attr('for'), newIndex));
                return;
            }
            if ($item.is('h4')) {
                // Update labels
                var index = newIndex + 1
                $item.text('Policy-Target '+index);
                return;
            }
            // Update other fields
            $item.attr('id', replaceTemplateIndex($item.attr('id'), newIndex));
            $item.attr('name', replaceTemplateIndex($item.attr('name'), newIndex));
        });

        // Append
        $('#subforms-container').append($newForm);
        $newForm.addClass('subform');
        $newForm.removeClass('is-hidden');
        $newForm.find('.removeBtn').click(removeForm);

        
    }

    
}




function flashes() {
    // Get the snackbar DIV
    var x = document.getElementById("snackbar");
    // Add the "show" class to DIV
    x.className = "show";
    // After 3 seconds, remove the show class from DIV
    setTimeout(function(){ x.className = x.className.replace("show", ""); }, 3000);
  } 

var adjusting = "this.style.width = ((this.value.length + 1) * 8) + 'px';"
  
$(document).ready(function() {
    clear(); // Clears the input at origin
    $(".input-adjust").attr("onkeypress", adjusting)
    $('.removeBtn').click(removeForm); // Removes undesired input
    $('#add').click(function(e) {
        addForm();
        return false;
    }); // Adds input to form
    flashes();
});
