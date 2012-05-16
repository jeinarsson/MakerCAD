-module(geometry_workers_app).

-behaviour(application).

%% Application callbacks
-export([start/2, stop/1]).

%% ===================================================================
%% Application callbacks
%% ===================================================================

start(_StartType, _StartArgs) ->
    {ok, SupervisorPid} = geometry_workers_sup:start_link(),

    {ok, NumberOfWorkers} = application:get_env(number_of_workers),
    lists:map(
    	fun(_) -> 
    		{ok, _} = supervisor:start_child(geometry_workers_sup, []) 
    	end,
    	lists:seq(1, NumberOfWorkers)),
    
    {ok, SupervisorPid}.

stop(_State) ->
    ok.
