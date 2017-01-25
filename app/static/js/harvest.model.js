harvest.model = (function () {
	var

		configMap = {},

		stateMap  = {},

		update,
		pending,		
		initModule;

	pending_db = TAFFY();

	update = function ( data, source ) {
		data.forEach( function ( pendingStr ) {
			pendingObj = JSON.parse(pendingStr);
			pendingObj.source = source;
			pending_db.insert( pendingObj );
		})
	};

	pending = (function () {
		var
			get_pending;

		get = function ( paramObj ) {
			var data;

			data = pending_db( paramObj ).first();
			return data;
		};

		all = function ( paramObj ) {
			var data;

			data = pending_db( paramObj ).get();
			return data;
		}

		return {
			get : get,
			all : all
		}
	}());

	initModule = function () {};

	return {
		initModule : initModule,
		pending : pending,
		update : update
	};
}());