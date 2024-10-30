// Copyright (c) 2024, Atom Global and contributors
// For license information, please see license.txt

frappe.ui.form.on('Weigh Slip', {
	// refresh: function(frm) {

	// }
});


frappe.ui.form.on("Weighment Details", {
    weighment_details_add: function(frm, cdt, cdn) {
        var child = locals[cdt][cdn];  // Current child row
        child.user = frappe.session.user_fullname;  // Set the user field to the session user
        frm.refresh_field("weighment_details");  // Refresh the child table to reflect the changes
    }
});


frappe.ui.form.on("Weigh Slip", {
    card_no: function(frm) {
        // Jab form refresh ho, session user ka naam operator field mein set karain
        frm.set_value("operator", frappe.session.user_fullname);  // Set the operator field
        frm.refresh_field("operator");  // Refresh to reflect changes
    }
});

frappe.ui.form.on('Weigh Slip', {
    scale_in_front: function(frm) {
        update_front_image_preview(frm);
    },
    scale_in_back: function(frm) {
        update_back_image_preview(frm);
    },
    refresh: function(frm){
        update_front_image_preview(frm);
        update_back_image_preview(frm);
        update_scale_out_front_preview(frm);
        update_scale_out_back_preview(frm);
    },
    scale_out_front: function(frm){
        update_scale_out_back_preview(frm);
    },
    scale_out_back: function(frm){
        update_scale_out_back_preview(frm);
    }
});

function update_front_image_preview(frm) {
    // Get the image URL for "scale_in_front"
    var front_image_url = frm.doc.scale_in_front;

    // Create HTML content for the image preview
    var html_content = '';
    if (front_image_url) {
        html_content = `<img src="${front_image_url}" style="width: 400px; height: 300px;" title="Front Image">`; // Adjust size as needed
    }

    // Display the front image in the corresponding HTML field
    frm.set_df_property('scale_in_front_preview', 'options', html_content); // Set the HTML content to display the image
    frm.refresh_field('scale_in_front_preview'); // Refresh to apply changes
}

function update_back_image_preview(frm) {
    // Get the image URL for "scale_in_back"
    var back_image_url = frm.doc.scale_in_back;

    // Create HTML content for the image preview
    var html_content = '';
    if (back_image_url) {
        html_content = `<img src="${back_image_url}" style="width: 400px; height: 300px;" title="Back Image">`; // Adjust size as needed
    }

    // Display the back image in the corresponding HTML field
    frm.set_df_property('scale_in_back_preview', 'options', html_content); // Set the HTML content to display the image
    frm.refresh_field('scale_in_back_preview'); // Refresh to apply changes
}


function update_scale_out_front_preview(frm) {
    // Get the image URL for "scale_in_front"
    var front_image_url = frm.doc.scale_out_front;

    // Create HTML content for the image preview
    var html_content = '';
    if (front_image_url) {
        html_content = `<img src="${front_image_url}" style="width: 400px; height: 300px;" title="Front Image">`; // Adjust size as needed
    }

    // Display the front image in the corresponding HTML field
    frm.set_df_property('scale_out_front_preview', 'options', html_content); // Set the HTML content to display the image
    frm.refresh_field('scale_out_front_preview'); // Refresh to apply changes
}

function update_scale_out_back_preview(frm) {
    // Get the image URL for "scale_in_back"
    var back_image_url = frm.doc.scale_out_back;

    // Create HTML content for the image preview
    var html_content = '';
    if (back_image_url) {
        html_content = `<img src="${back_image_url}" style="width: 400px; height: 300px;" title="Back Image">`; // Adjust size as needed
    }

    // Display the back image in the corresponding HTML field
    frm.set_df_property('scale_out_back_preview', 'options', html_content); // Set the HTML content to display the image
    frm.refresh_field('scale_out_back_preview'); // Refresh to apply changes
}