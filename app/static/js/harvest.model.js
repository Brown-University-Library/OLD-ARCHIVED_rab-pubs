harvest.model = (function () {
	var

		configMap = {},

		stateMap  = {},

		update,
		pending,		
		initModule;

	pending_db = TAFFY();
	queries_db = TAFFY();
        params_db = TAFFY();

	update_pending = function ( data, source ) {
		data.forEach( function ( pendingObj ) {
			pendingObj.source = source;
			pending_db.insert( pendingObj );
		})
		$( window ).trigger( 'pendingQueryCompleted', source );
	};

	update_queries = function ( data, source ) {
		//var params = data.params;
		//params_db.insert( {'source': source, 'params': params });
		//var queries = data.queries;
		//queries.forEach( function ( queryObj ) {
		data.forEach( function ( queryObj ) {
			queries_db.insert( { 	'rabid'	: queryObj.rabid,
						'source': source,
						'data'	: queryObj.data,
						'params' : queryObj.params,
						'display': queryObj.display } );
		})
		$( window ).trigger( 'queriesQueryCompleted', source );
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

	queries = (function () {
		var
			get, all,
			create,
			initialize;

		get = function ( paramObj ) {
			var data;

			data = queries_db( paramObj ).first();
			return data;
		};

		all = function ( paramObj ) {
			var data;

			data = queries_db( paramObj ).get();
			return data;
		};

		create = function ( sourceRabid, dataObj ) {
			harvest.data.postQuery( sourceRabid, dataObj);
		};

		save = function ( sourceRabid, dataObj ) {

		};

		initialize = function ( sourceRabid ) {
			harvest.data.getQueries( sourceRabid );
		};

		return {
			get : get,
			all : all,
			create: create,
			initialize : initialize
		};
	}());

        params = (function () {
		var
			get, all,
			create,
			initialize;

		get = function ( paramObj ) {
			var data;

			data = params_db( paramObj ).first();
			return data;
		};

		all = function ( paramObj ) {
			var data;

			data = params_db( paramObj ).get();
			return data;
		};

		return {
			get : get,
			all : all,
		};
	}());

	initModule = function () {};

	return {
		initModule : initModule,
		pending : pending,
		queries : queries,
		params : params,
		update_queries : update_queries,
		update_pending : update_pending
	};
}());
