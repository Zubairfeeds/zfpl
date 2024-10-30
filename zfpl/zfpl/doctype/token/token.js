// Copyright (c) 2024, Atom Global and contributors
// For license information, please see license.txt

// frappe.ui.form.on('Token', {
// 	// refresh: function(frm) {

// 	// }
// });


frappe.ui.form.on('Token', {
	refresh: function (frm) {
		if (frm.doc.docstatus == 1 && frm.doc.document_type == "Purchase Order") {
			frm.add_custom_button(__("GRN"), function () {
				makeGrn(frm);
			}, __('Create')).css({ 'background-color': 'red', 'color': 'white', 'border-radius': 20 }); // Set background color and text color directly
		}
		else if (frm.doc.docstatus == 1 && frm.doc.document_type == "Sales Order") {
			frm.add_custom_button(__("Delivery Note"), function () {
				makeDn(frm);
			}, __('Create')).css({ 'background-color': 'red', 'color': 'white', 'border-radius': 20 }); // Set background color and text color directly
		}
	}
});

function makeGrn(frm) {
	frappe.model.open_mapped_doc({
		method: 'zfpl.zfpl.doctype.token.token.make_grn',
		frm: frm
	});
}

function makeDn(frm) {
	frappe.model.open_mapped_doc({
		method: 'zfpl.zfpl.doctype.token.token.makeDn',
		frm: frm
	});
}


// frappe.ui.form("Token", {
// 	before_save: function(frm){
// 		if(frm.doc.weigh_slip){
// 			frappe.call({
// 				method: 'frappe.client.set_value',
// 				args:{
// 					'doctype': 'Weigh Slip',
// 					'name': frm.doc.weigh_slip,
// 					'fieldname': 'status',
// 					'value': 'Atteched'
// 				},
// 				callback: function(response){
// 					console.log('Weigh Slip status updated to Attached');
//                 }
// 			});
// 		}
// 	},
// 	onload: function(frm){
// 		frm.set_query ('weigh_slip', function(){
// 		return{
// 			filters:{
// 				'status': "Open"
// 			}
// 		};
// 	});
// 	}
// });

frappe.ui.form.on("Token", {
    before_save: function(frm) {
        if (frm.doc.weigh_slip) {
            frappe.call({
                method: 'frappe.client.set_value',
                args: {
                    'doctype': 'Weigh Slip',
                    'name': frm.doc.weigh_slip,
                    'fieldname': 'status',
                    'value': 'Attached'
                },
                callback: function(response) {
                    console.log('Weigh Slip status updated to Attached');
                },
                error: function(error) {
                    console.error('Error updating Weigh Slip status:', error);
                }
            });
        }
    },
    refresh: function(frm) {
        frm.set_query('weigh_slip', function() {
            return {
                filters: {
                    'status': 'Open'  // Ensure correct field name
                }
            };
        });
    }
});



frappe.ui.form.on('Token', {
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
        update_scale_out_front_preview(frm);
    },
    scale_out_back: function(frm){
        update_scale_out_back_preview(frm);
    },
    tare_weight: function(frm){
        calculate_net_weight(frm);
    },
    gross_weight: function(frm){
        calculate_net_weight(frm);
    },

    scale_in_weight: function(frm){
        set_ist_weight(frm);
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
    // Get the image URL for "scale_out_front"
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
    // Get the image URL for "scale_out_back"
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

function calculate_net_weight(frm) {
    let gross_weight = frm.doc.gross_weight // Get the gross weight from the form
    let tare_weight = frm.doc.tare_weight // Get the tare weight from the form

    // Calculate the net weight
    let net_weight = gross_weight - tare_weight;

    // Set the net weight back to the form
    frm.set_value('net_weight', net_weight);
}

function set_ist_weight(frm){
    let ist_weight = frm.doc.scale_in_weight
    frm.set_value('ist_weight', ist_weight);
}