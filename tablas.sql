-- This script was generated by the ERD tool in pgAdmin 4.
-- Please log an issue at https://github.com/pgadmin-org/pgadmin4/issues/new/choose if you find any bugs, including reproduction steps.
BEGIN;


CREATE TABLE IF NOT EXISTS public.pokemones
(
    id serial NOT NULL,
    nombre character varying NOT NULL,
    tipo character varying NOT NULL,
    habilidad character varying NOT NULL,
    numero integer NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.entrenadores
(
    id serial NOT NULL,
    nombre character varying NOT NULL,
    PRIMARY KEY (id)
);


CREATE TABLE IF NOT EXISTS public.equipos
(
    id serial NOT NULL,
    pokemon1_id integer NOT NULL,
    pokemon2_id integer NOT NULL,
    pokemon3_id integer NOT NULL,
    entrenador_id integer NOT NULL,
    batalla_id integer NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS public.batallas
(
    id serial NOT NULL,
    equipo1_id integer NOT NULL,
    equipo2_id integer NOT NULL,
    ganador integer NOT NULL,
    fecha date NOT NULL,
    PRIMARY KEY (id)
);



ALTER TABLE IF EXISTS public.equipos
    ADD CONSTRAINT "FK_pokemon1_id" FOREIGN KEY (pokemon1_id)
    REFERENCES public.pokemones (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.equipos
    ADD CONSTRAINT "FK_pokemon2_id" FOREIGN KEY (pokemon2_id)
    REFERENCES public.pokemones (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.equipos
    ADD CONSTRAINT "FK_pokemon3_id" FOREIGN KEY (pokemon3_id)
    REFERENCES public.pokemones (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.equipos
    ADD CONSTRAINT "FK_entrenador_id" FOREIGN KEY (entrenador_id)
    REFERENCES public.entrenadores (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.equipos
    ADD CONSTRAINT "FK_batalla_id" FOREIGN KEY (batalla_id)
    REFERENCES public.batallas (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.batallas
    ADD CONSTRAINT "FK_equipo1" FOREIGN KEY (equipo1_id)
    REFERENCES public.equipos (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.batallas
    ADD CONSTRAINT "FK_equipo2" FOREIGN KEY (equipo2_id)
    REFERENCES public.equipos (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;


ALTER TABLE IF EXISTS public.batallas
    ADD CONSTRAINT "FK_ganador" FOREIGN KEY (ganador)
    REFERENCES public.equipos (id) MATCH SIMPLE
    ON UPDATE NO ACTION
    ON DELETE CASCADE
    NOT VALID;

END;