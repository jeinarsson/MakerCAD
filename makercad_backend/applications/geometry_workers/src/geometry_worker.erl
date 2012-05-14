-module(geometry_worker).
-behaviour(gen_server).

%% ------------------------------------------------------------------
%% API Function Exports
%% ------------------------------------------------------------------

-export([start_link/0, stop/0, compute/2]).

%% ------------------------------------------------------------------
%% gen_server Function Exports
%% ------------------------------------------------------------------

-export([init/1, handle_call/3, handle_cast/2, handle_info/2,
         terminate/2, code_change/3]).

%% ------------------------------------------------------------------
%% API Function Definitions
%% ------------------------------------------------------------------

start_link() ->
    gen_server:start_link(?MODULE, [], []).

stop() ->
	gen_server:call(?MODULE, stop).

compute(Pid, Blob) ->
	lager:info("Sending gen_server:call on: ~p",[Blob]),
	gen_server:call(Pid, {compute, Blob}, infinity).


%% ------------------------------------------------------------------
%% gen_server Function Definitions
%% ------------------------------------------------------------------

-record(state, {port}).

init(_Args) ->
	Worker_executable = filename:absname(filename:join([code:priv_dir(geometry_workers)] ++ ["makercad_worker.exe"])),
	lager:info("Opening Port to ~p", [Worker_executable]),
	process_flag(trap_exit, true),
	Port = open_port({spawn_executable, Worker_executable},
		[{packet,4}, {cd, filename:dirname(Worker_executable)}]),
    {ok, #state{port=Port}}.

handle_call(stop, _From, State) ->
	{stop, normal, stopped, State};

handle_call({compute, Blob}, _From, State) ->
	lager:info("WTF",[]),
	lager:info("Compute call on: ~p",[Blob]),
	Port = State#state.port,
	Port ! {self(), {command, Blob}},
	receive
		{Port, {data, Data}} ->
		    {reply, Data, State};
		{'EXIT', Port, Reason} ->
			{stop, {error, Reason}, State}
	after 600 ->
		{stop, {error, compute_timeout}, State}
	end;

handle_call(testcall, _From, State) ->
	lager:info("testcall"),
	{reply,42,State};

handle_call(Request, _From, State) ->
	lager:warning("~p unexpected call: ~p", [?MODULE, Request]),
	{reply, unexpected_call, State}.

handle_cast(Msg, State) ->
	lager:warning("~p unexpected cast: ~p", [?MODULE, Msg]),
    {noreply, State}.


handle_info({'EXIT', Port, Reason}, State) when Port =:= State#state.port ->
	lager:info("~p port crashed => terminating worker: ~p", [?MODULE, Reason]),
    {stop, port_crashed, State};

handle_info(Info, State) ->
	lager:warning("~p unexpected info: ~p", [?MODULE, Info]),
    {noreply, State}.

terminate(Reason, State) ->
	lager:info("terminating ~p: ~p", [?MODULE, Reason]),
	Port = State#state.port,
	Port ! {self(), close},
	receive
		{Port, closed} ->
			ok;
		Err ->
			throw(Err)
	after 5000 ->
		throw(port_close_timeout)
	end.
    

code_change(_OldVsn, State, _Extra) ->
    {ok, State}.

%% ------------------------------------------------------------------
%% Internal Function Definitions
%% ------------------------------------------------------------------

