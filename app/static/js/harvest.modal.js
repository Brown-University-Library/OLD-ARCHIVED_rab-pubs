harvest.modal = (function () {

	var configMap = {
		main_html : String()
			+ '<div class="dynamic-modal modal fade" tabindex="-1" role="dialog">'
				+ '<div class="modal-dialog" role="document">'
					+ '<div class="modal-content">'
						+ '<div class="modal-header">'
							+ '<h5 class="modal-title"></h5>'
                			+ '<button type="button" class="close" data-dismiss="modal">'
								+ '<span aria-hidden="true">&times;</span>'
							+ '</button>'
						+ '</div>'
						+ '<div class="modal-body">'
						+ '</div>'
						+ '<div class="modal-footer">'
							+ '<button type="button" class="modal-close btn btn-secondary" data-dismiss="modal">Close</button>'
						+ '</div>'
		            + '</div>'
				+ '</div>'
			+ '</div>'
	},

	stateMap = {
		$append_target : null
	},

	jqueryMap = {},

	launchPendingDetail, launchProcessDetail,
	resetModal,
	setJqueryMap, initModule;

	setJqueryMap = function () {
		var
			$append_target = stateMap.$append_target,
			$modal = $append_target.find('.dynamic-modal');


		jqueryMap = {
			$modal : $modal,
			$modal_title : $modal.find('.modal-title'),
			$modal_header : $modal.find('.modal-header'),
			$modal_body : $modal.find('.modal-body'),
			$modal_footer : $modal.find('.modal-footer')
		};

	};

	resetModal = function () {
		var
			$modal_title,
			$modal_body, $modal_footer;

		$modal_title = jqueryMap.$modal_title;
		$modal_body = jqueryMap.$modal_body;
		$modal_footer = jqueryMap.$modal_footer;

		$modal_title.empty();
		$modal_body.empty();
		$modal_footer.children().not('.modal-close').remove();

	};

	launchPendingDetail = function ( pendingObj ) {
		var
			$modal, $modal_title, $modal_body,
			$table, $tbody;

		resetModal();

		$modal = jqueryMap.$modal;
		$modal_title = jqueryMap.$modal_title;
		$modal_body = jqueryMap.$modal_body;

		$modal_title.text('Citation Details');

		$table = $('<table/>', {'class': 'table'});
		$tbody = $('<tbody/>');

		pendingObj.display.details.forEach( function( detailsObj ) {
			var $tr = $('<tr/>');
			var $key = $('<th/>', { 'scope': 'row',
								'text' : detailsObj.key });
			var $value = $('<td/>', { 'text' : detailsObj.value });

			$tr.append($key);
			$tr.append($value);
			$tbody.append($tr);
		});

		$table.append($tbody);
		$modal_body.append($table);
		$modal.modal('show');
	};

	launchProcessDetail = function ( processObj, paramOptList ) {
		var
			$modal, $modal_title, $modal_body,
			operator_list,
			$form;

		resetModal();

		operator_list = [ 'AND', 'OR', 'NOT' ];

		$modal = jqueryMap.$modal;
		$modal_title = jqueryMap.$modal_title;
		$modal_body = jqueryMap.$modal_body;

		$modal_title.text( processObj.display );

		$form = $('<form/>');

		processObj.data.parameters.forEach( function ( param, idx ) {
			var $div, $select_opr, $select_attr, $input, $rmv;

			$div = $('<div/>',	{	'class': "form-group query-row",
									'data-index': idx });
			$select_attr = $('<select/>', {	'class': 'query-att form-control'});
			$input = $('<input/>',	{	'class': 'query-val form-control',
										'type': 'text',
										'value': param.value } );

			paramOptList.forEach( function( opt ) {
				var $option;
	        	$option = $('<option/>', {	'value': opt,
	                                  		'text' : opt });
	        	if ( param.attribute === opt ) {
	        		$option.prop('selected', 'selected');
	        	}

	        	$select_attr.append($option);
			}); 

			if ( idx === 0) {
				$select_opr = $('<span/>', { 'class': 'query-opr' });
				$rmv = $('<span/>', {'class': 'query-rmv' });
			} else {
				$select_opr = $('<select/>', { 'class': 'query-opr form-control'});

				operator_list.forEach( function( opt ) {
					var $option;
		        	$option = $('<option/>', {	'value': opt,
		                                  		'text' : opt });
		        	if ( param.operator === opt ) {
		        		$option.prop('selected', 'selected');
		        	}

		        	$select_opr.append($option);
				});

				$rmv = $('<button/>', {'class': 'btn btn-warning query-rmv',
								'type': 'button',
								'html': '\&times\;'});
			}

			$form.append($div);
		});

		$modal_body.append($form);
		$modal.modal('show');
	};

	initModule = function ( $appendTarget ) {

		stateMap.$append_target = $appendTarget;

		$appendTarget.append( configMap.main_html );
		setJqueryMap();

	};

	return {
		initModule : initModule,
		launchPendingDetail : launchPendingDetail,
		launchProcessDetail : launchProcessDetail
	};
}());
