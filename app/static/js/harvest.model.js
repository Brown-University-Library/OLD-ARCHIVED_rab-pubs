harvest.model = (function () {
	var

		configMap = {},

		stateMap  = {},

		update,
		pending,		
		initModule;

	pending_db = TAFFY();

	update_pending = function ( data, source ) {
		data.forEach( function ( pendingObj ) {
			pendingObj.source = source;
			pending_db.insert( pendingObj );
		})
		$( window ).trigger( 'pendingQueryCompleted', source );
	};

	pending = (function () {
		var
			get, all, initialize;

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

		initialize = function ( sourceRabid ) {
			harvest.data.getPending( sourceRabid );
		}

		return {
			get : get,
			all : all,
			initialize : initialize
		}
	}());

	initModule = function () {};

	return {
		initModule : initModule,
		pending : pending,
		update_pending : update_pending
	};
}());