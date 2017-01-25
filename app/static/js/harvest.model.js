harvest.model = (function () {
	var

		configMap = {},

		stateMap  = {},

		update,
		pending,		
		initModule;

	update = (function ( data, source ) {
		stateMap[source] = data;
	});

	pending = (function () {
		var
			get_pending;

		get_pending = function ( source ) {
			var data;

			data = stateMap[source];
			return data;
		};

		return {
			get_pending : get_pending
		}
	}());

	initModule = function () {};

	return {
		initModule : initModule,
		pending : pending,
		update : update
	};
}());