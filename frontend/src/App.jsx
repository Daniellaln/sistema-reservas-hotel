import React, { useEffect, useRef, useState } from "react";
import { createRoot } from "react-dom/client";
import {
  CalendarDays,
  Users,
  DoorOpen,
  Wallet,
  Clock3,
  History,
  Settings2,
  Search,
  Plus,
  ArrowUpRight,
  ArrowDownToLine,
  ArrowUpFromLine,
  ChevronRight,
  X,
  RefreshCw,
  ArrowLeftRight,
  Hotel,
  CheckCircle2,
  AlertCircle,
  ChartNoAxesCombined,
} from "lucide-react";
import "./style.css";
import LiquidGlass from "liquid-glass-react";

const money = (n) =>
  new Intl.NumberFormat("es-PE", { style: "currency", currency: "PEN" }).format(
    n / 100,
  );
const fecha = (s) =>
  s
    ? new Intl.DateTimeFormat("es-PE", {
        day: "2-digit",
        month: "short",
      }).format(new Date(s + "T12:00:00"))
    : "—";
const nav = [
  ["Agenda", CalendarDays],
  ["Huéspedes", Users],
  ["Habitaciones", DoorOpen],
  ["Cobros", Wallet],
  ["Espera", Clock3],
  ["Reportes", ChartNoAxesCombined],
  ["Historial", History],
  ["Datos", Settings2],
];
async function bridge(method, ...args) {
  if (!window.pywebview?.api) {
    await new Promise((resolve, reject) => {
      let timer = setTimeout(() => {
        window.removeEventListener("pywebviewready", ready);
        reject(
          Error("Abre la aplicación con ABRIR.bat para conectar con Python."),
        );
      }, 10000);
      function ready() {
        clearTimeout(timer);
        resolve();
      }
      window.addEventListener("pywebviewready", ready, { once: true });
    });
  }
  return window.pywebview.api[method](...args);
}
function IconButton({ children, ...props }) {
  return (
    <button type="button" className="icon-button" {...props}>
      {children}
    </button>
  );
}
function Estado({ value }) {
  return (
    <span
      className={
        "status " +
        ({
          Confirmada: "confirmed",
          "En estancia": "staying",
          Finalizada: "finished",
          Cancelada: "canceled",
          Disponible: "available",
          Ocupada: "staying",
          Mantenimiento: "canceled",
        }[value] || "")
      }
    >
      {value}
    </span>
  );
}
function Empty({ title, text, action }) {
  return (
    <div className="empty">
      <CalendarDays size={30} />
      <h3>{title}</h3>
      <p>{text}</p>
      {action}
    </div>
  );
}
function Field({ label, name, type = "text", children, ...props }) {
  return (
    <label className="field">
      <span>{label}</span>
      {children ? (
        <select name={name} required {...props}>
          {children}
        </select>
      ) : (
        <input name={name} type={type} required {...props} />
      )}
    </label>
  );
}
function App() {
  const [data, setData] = useState(null),
    [view, setView] = useState("Agenda"),
    [filter, setFilter] = useState("Activas"),
    [search, setSearch] = useState(""),
    [order, setOrder] = useState("entrada");
  const [panel, setPanel] = useState(null),
    [notice, setNotice] = useState(null),
    [confirm, setConfirm] = useState(null),
    [busy, setBusy] = useState(false),
    [quote, setQuote] = useState(null),
    [reverse, setReverse] = useState(true),
    [found, setFound] = useState(undefined),
    [bootError, setBootError] = useState(""),
    [report, setReport] = useState(null),
    [guestDni, setGuestDni] = useState(""),
    [guestName, setGuestName] = useState(""),
    [moreOpen, setMoreOpen] = useState(false),
    [reducedMotion, setReducedMotion] = useState(false);
  const formRef = useRef(null),
    panelRef = useRef(null),
    dialogRef = useRef(null),
    seq = useRef(0),
    pending = useRef(false),
    focusRef = useRef(null),
    navRef = useRef(null),
    moreRef = useRef(null);
  useEffect(() => {
    const preference = window.matchMedia("(prefers-reduced-motion: reduce)");
    const update = () => setReducedMotion(preference.matches);
    update();
    preference.addEventListener("change", update);
    return () => preference.removeEventListener("change", update);
  }, []);
  useEffect(() => {
    if (!moreOpen) return;
    function outside(e) {
      if (!navRef.current?.contains(e.target)) setMoreOpen(false);
    }
    function escape(e) {
      if (e.key === "Escape") {
        setMoreOpen(false);
        moreRef.current?.focus();
      }
    }
    function focusOutside(e) {
      if (!navRef.current?.contains(e.target)) setMoreOpen(false);
    }
    document.addEventListener("pointerdown", outside, true);
    document.addEventListener("keydown", escape);
    document.addEventListener("focusin", focusOutside);
    return () => {
      document.removeEventListener("pointerdown", outside, true);
      document.removeEventListener("keydown", escape);
      document.removeEventListener("focusin", focusOutside);
    };
  }, [moreOpen]);
  useEffect(() => { setMoreOpen(false); }, [view, panel?.type]);
  async function refresh() {
    try {
      setData(await bridge("estado", order));
      setBootError("");
    } catch (e) {
      setBootError(e.message);
    }
  }
  useEffect(() => {
    refresh();
  }, [order]);
  useEffect(() => {
    if (panel) {
      panelRef.current?.querySelector('input:not([type="hidden"]),select,button')?.focus();
      cotizar();
    } else {
      if (focusRef.current?.isConnected) focusRef.current.focus();
      focusRef.current = null;
    }
  }, [panel?.type]);
  useEffect(() => {
    if (confirm) dialogRef.current?.showModal();
    else if (dialogRef.current?.open) dialogRef.current.close();
  }, [confirm]);
  useEffect(() => {
    function key(e) {
      if (e.key === "Escape" && !busy) {
        if (confirm) setConfirm(null);
        else setPanel(null);
      }
    }
    window.addEventListener("keydown", key);
    return () => window.removeEventListener("keydown", key);
  }, [busy, confirm]);
  function keepFocus(e) {
    if (e.key !== "Tab" || confirm) return;
    const controls = [...panelRef.current.querySelectorAll('button:not(:disabled),input:not(:disabled):not([type="hidden"]),select:not(:disabled)')];
    if (!controls.length) return;
    const first = controls[0], last = controls[controls.length - 1];
    if (e.shiftKey && document.activeElement === first) {
      e.preventDefault(); last.focus();
    } else if (!e.shiftKey && document.activeElement === last) {
      e.preventDefault(); first.focus();
    }
  }
  function open(type, record = null) {
    if (!panel) focusRef.current = document.activeElement;
    seq.current++;
    setPanel({ type, record });
    setGuestDni(record?.dni || "");
    setGuestName("");
    setNotice(null);
    setQuote(null);
  }
  async function operate(action, payload, close = true) {
    if (pending.current || !data) return false;
    pending.current = true;
    setBusy(true);
    try {
      const result = await bridge("operar", action, payload, data.revision);
      setData(result.datos);
      setReport(null);
      setNotice({ error: !result.ok, text: result.mensaje });
      if (result.ok && close) setPanel(null);
      return result.ok;
    } catch (e) {
      setNotice({ error: true, text: e.message });
      return false;
    } finally {
      pending.current = false;
      setBusy(false);
    }
  }
  async function file(method) {
    if (pending.current) return;
    pending.current = true;
    setBusy(true);
    try {
      const result = await bridge(
        method,
        ...(method === "importar" ? [data.revision] : []),
      );
      if (result.datos) setData(result.datos);
      setReport(null);
      setNotice({ error: !result.ok, text: result.mensaje });
    } catch (e) {
      setNotice({ error: true, text: e.message });
    } finally {
      pending.current = false;
      setBusy(false);
    }
  }
  function ask(title, text, run) {
    setConfirm({ title, text, run });
  }
  function change(r, estado) {
    if (estado === "En estancia") {
      operate("estado", { id: r.id, estado });
      return;
    }
    ask(
      estado === "En estancia"
        ? "Recibir al huésped"
        : estado === "Finalizada"
          ? "Finalizar la estadía"
          : "Cancelar reserva",
      `${r.nombre} · Habitación ${r.habitacion}. ${estado === "Cancelada" ? "Se conservará la reserva en el historial. La cancelación con pagos está bloqueada." : estado === "Finalizada" ? "El saldo debe estar pagado." : "La fecha de hoy debe estar dentro de la estadía."}`,
      () => operate("estado", { id: r.id, estado }),
    );
  }
  async function submit(e) {
    e.preventDefault();
    const p = Object.fromEntries(new FormData(e.currentTarget));
    const action = panel.type === "cobro" ? "pago" : panel.type;
    const ok = await operate(action, p);
    if (ok && action === "reserva") {
      setView("Agenda");
      setFilter("Activas");
      setSearch("");
    }
  }
  async function cotizar() {
    if (panel?.type !== "reserva" || !formRef.current) return;
    const n = ++seq.current,
      p = Object.fromEntries(new FormData(formRef.current));
    if (!p.numero || !p.entrada || !p.salida) {
      setQuote(null);
      return;
    }
    setQuote(null);
    try {
      const result = await bridge(
        "cotizar",
        p.numero,
        p.entrada,
        p.salida,
        p.personas,
      );
      if (n === seq.current) setQuote(result);
    } catch (e) {
      if (n === seq.current) setQuote({ ok: false, mensaje: e.message });
    }
  }
  if (!data)
    return (
      <div className="boot">
        <div className="brand-mark">
          <Hotel />
        </div>
        <h1>Sistema de Gestión de Reservas de Hotel</h1>
        <p>{bootError || "Conectando con Python…"}</p>
        {bootError && <button onClick={refresh}>Reintentar</button>}
      </div>
    );
  const term = search.trim().toLocaleLowerCase("es");
  const knownGuest = data.huespedes.find((h) => h.dni === guestDni);
  const tomorrow = new Date(data.hoy + "T12:00:00");
  tomorrow.setDate(tomorrow.getDate() + 1);
  const nextDay = `${tomorrow.getFullYear()}-${String(tomorrow.getMonth()+1).padStart(2,"0")}-${String(tomorrow.getDate()).padStart(2,"0")}`;
  const matches = (...items) =>
    items.some((x) =>
      String(x ?? "")
        .toLocaleLowerCase("es")
        .includes(term),
    );
  const reservas = data.reservas.filter(
    (r) =>
      matches(r.nombre, r.dni, r.habitacion, r.id) &&
      {
        Activas: ["Confirmada", "En estancia"].includes(r.estado),
        Llegadas: r.entrada === data.hoy && r.estado === "Confirmada",
        "En estancia": r.estado === "En estancia",
        Salidas: r.salida <= data.hoy && r.estado === "En estancia",
        Todas: true,
      }[filter],
  );
  const tabs = ["Activas", "Llegadas", "Todas"];
  const eligible = data.reservas.filter(
    (r) => ["Confirmada", "En estancia"].includes(r.estado) && r.saldo > 0,
  );
  function peopleOptions() {
    return (
      <>
        <option value="">Selecciona un huésped</option>
        {data.huespedes.map((h) => (
          <option key={h.dni} value={h.dni}>
            {h.nombre} · {h.dni}
          </option>
        ))}
      </>
    );
  }
  function roomOptions() {
    return (
      <>
        <option value="">Selecciona una habitación</option>
        {data.habitaciones.map((h) => (
          <option key={h.numero} value={h.numero}>
            {h.numero} · {h.tipo} · {money(h.tarifa)}
          </option>
        ))}
      </>
    );
  }
  const rows = (headers, body) => (
    <div className="table-scroll">
      <table>
        <thead>
          <tr>
            {headers.map((h) => (
              <th key={h}>{h}</th>
            ))}
          </tr>
        </thead>
        <tbody>{body}</tbody>
      </table>
    </div>
  );
  const add = () =>
    open(
      {
        Agenda: "reserva",
        Huéspedes: "huesped",
        Habitaciones: "habitacion",
        Cobros: "cobro",
        Espera: "espera",
      }[view],
    );
  const canAdd = [
    "Agenda",
    "Huéspedes",
    "Habitaciones",
    "Cobros",
    "Espera",
  ].includes(view);
  const addText = {
    Agenda: "Nueva reserva",
    Huéspedes: "Registrar huésped",
    Habitaciones: "Nueva habitación",
    Cobros: "Registrar pago",
    Espera: "Añadir solicitud",
  }[view];
  return (
    <div className="app-shell">
      <aside className="sidebar" inert={panel ? true : undefined}>
        <div className="brand">
          <span className="brand-mark">
            <Hotel size={22} />
          </span>
          <div>
            <strong>Hotel</strong>
            <small>Gestión de reservas</small>
          </div>
        </div>
        <div className="nav-host" ref={navRef}><div className="liquid-nav"><LiquidGlass mode="shader" displacementScale={40} blurAmount={0.04} saturation={125} aberrationIntensity={1.6} elasticity={reducedMotion ? 0 : 0.25} cornerRadius={28} padding="6px" overLight={false} style={{position:"absolute",top:"50%",left:"50%"}}><nav aria-label="Secciones">
          {nav.filter(([n]) => ["Agenda", "Habitaciones"].includes(n)).map(([n, I]) => (
            <button
              key={n}
              disabled={busy}
              aria-current={view === n ? "page" : undefined}
              className={view === n ? "selected" : ""}
              onClick={() => {
                setMoreOpen(false);
                setView(n);
                setSearch("");
                setPanel(null);
                setFound(undefined);
              }}
            >
              <I size={18} />
              {n === "Agenda" ? "Recepción" : n}
              {n === "Espera" && data.espera.length > 0 && (
                <b>{data.espera.length}</b>
              )}
            </button>
          ))}
          <button ref={moreRef} aria-expanded={moreOpen} aria-controls="more-options" onClick={()=>setMoreOpen(!moreOpen)}><Settings2 size={17}/>Más</button>
        </nav></LiquidGlass></div>
        {moreOpen && <div className="more-popover" id="more-options" aria-label="Más secciones">
          {nav.filter(([n]) => !["Agenda", "Habitaciones"].includes(n)).map(([n,I]) => <button key={n} disabled={busy} onClick={()=>{setView(n);setSearch("");setPanel(null);setFound(undefined);setMoreOpen(false);moreRef.current?.focus();}}><I size={19}/>{n}</button>)}
        </div>}</div>
      </aside>
      <main className="main" inert={panel ? true : undefined}>
        <header className="topbar">
          <div className="breadcrumb">
            Hotel <ChevronRight size={14} />
            <span>{view}</span>
          </div>
          <div className="top-right">
            <span className="save-dot" />
            Guardado en este equipo
            <IconButton
              aria-label="Actualizar datos"
              title="Actualizar"
              onClick={refresh}
            >
              <RefreshCw size={16} />
            </IconButton>
          </div>
        </header>
        <section className="page-heading">
          <div>
            <h1>
              {view === "Agenda"
                ? "Recepción"
                : view === "Datos"
                  ? "Datos y estructuras"
                  : view === "Espera"
                    ? "Lista de espera"
                    : view}
            </h1>
            <p>
              {
                {
                  Agenda:
                    "Reserva, recibe y cobra. Sin perder el hilo.",
                  Huéspedes: "Identificación y contacto para cada estadía.",
                  Habitaciones: "Tarifas, capacidad y estado de atención.",
                  Cobros:
                    "Pagos parciales, saldos claros y registro de ingresos.",
                  Reportes:
                    "Ingresos, llegadas y estado del hotel por período.",
                  Espera: "Cada solicitud conserva su turno de llegada.",
                  Historial: "Un registro de las operaciones del hotel.",
                  Datos: "Tus copias de seguridad y el motor del proyecto.",
                }[view]
              }
            </p>
          </div>
          {canAdd && (
            <button className="primary clay" disabled={busy} onClick={add}>
              <Plus size={17} />
              {addText}
            </button>
          )}
        </section>
        {notice && (
          <div
            className={"notice " + (notice.error ? "error" : "success")}
            role="status"
          >
            {notice.error ? (
              <AlertCircle size={17} />
            ) : (
              <CheckCircle2 size={17} />
            )}
            <span>{notice.text}</span>
            <IconButton
              aria-label="Cerrar mensaje"
              onClick={() => setNotice(null)}
            >
              <X size={15} />
            </IconButton>
          </div>
        )}
        {view === "Agenda" && (
          <>
            <div className="summary-strip">
              <div>
                <span>Estancias abiertas</span>
                <strong>{data.resumen.abiertas}</strong>
              </div>
              <div>
                <span>Llegadas de hoy</span>
                <strong>{data.resumen.llegadas}</strong>
              </div>
              <div>
                <span>Saldo por cobrar</span>
                <strong>{money(data.resumen.pendiente)}</strong>
              </div>
              <div className="today">
                <CalendarDays size={17} />
                {new Intl.DateTimeFormat("es-PE", {
                  day: "numeric",
                  month: "long",
                  year: "numeric",
                }).format(new Date(data.hoy + "T12:00:00"))}
              </div>
            </div>
            <div className="toolbar">
              <div className="tabs" role="group" aria-label="Filtrar reservas">
                {tabs.map((t) => (
                  <button
                    key={t}
                    className={filter === t ? "active" : ""}
                    onClick={() => setFilter(t)}
                  >
                    {t === "Activas" ? "En curso" : t === "Llegadas" ? "Hoy llegan" : t}
                  </button>
                ))}
              </div>
              <div className="tools">
                <label className="search">
                  <Search size={16} />
                  <input
                    aria-label="Buscar reservas"
                    placeholder="Nombre, DNI o habitación"
                    value={search}
                    onChange={(e) => setSearch(e.target.value)}
                  />
                </label>
                <select
                  aria-label="Ordenar reservas"
                  value={order}
                  onChange={(e) => setOrder(e.target.value)}
                >
                  <option value="entrada">Por llegada</option>
                  <option value="total">Por importe</option>
                </select>
              </div>
            </div>
            {reservas.length ? (
              rows(
                [
                  "Huésped / reserva",
                  "Habitación",
                  "Estadía",
                  "Total / saldo",
                  "Estado",
                  "Acciones",
                ],
                reservas.map((r) => (
                  <tr key={r.id}>
                    <td>
                      <button
                        className="text-link"
                        onClick={() => open("detalle", r)}
                      >
                        {r.nombre}
                      </button>
                      <small>
                        {r.dni} · {r.id.slice(0, 8)}
                      </small>
                    </td>
                    <td>
                      <span className="room-number">{r.habitacion}</span>
                      <small>
                        {r.personas} {r.personas === 1 ? "persona" : "personas"}
                      </small>
                    </td>
                    <td>
                      <strong className="date-range">
                        {fecha(r.entrada)} <span>→</span> {fecha(r.salida)}
                      </strong>
                      <small>
                        {r.noches} {r.noches === 1 ? "noche" : "noches"}
                        {r.salida <= data.hoy && r.estado === "En estancia"
                          ? " · salida pendiente"
                          : ""}
                      </small>
                    </td>
                    <td>
                      <strong>{money(r.total)}</strong>
                      <small className={r.saldo > 0 && r.estado !== "Cancelada" ? "balance" : ""}>
                        {r.estado === "Cancelada" ? "Sin saldo exigible" : r.saldo ? money(r.saldo) + " pendiente" : "Pagado"}
                      </small>
                    </td>
                    <td>
                      <Estado value={r.estado} />
                      {r.estado === "Confirmada" && r.salida <= data.hoy && (
                        <small className="balance">Reserva vencida</small>
                      )}
                    </td>
                    <td>
                      <div className="row-actions">
                        {r.saldo > 0 &&
                          r.estado === "En estancia" && (
                            <button
                              disabled={busy}
                              onClick={() => open("cobro", r)}
                            >
                              Cobrar
                            </button>
                          )}
                        {r.estado === "Confirmada" && (
                          <button
                            disabled={busy}
                            onClick={() => r.entrada <= data.hoy && data.hoy < r.salida ? change(r, "En estancia") : open("detalle", r)}
                          >
                            {r.entrada <= data.hoy && data.hoy < r.salida ? "Recibir" : "Ver"} <ArrowUpRight size={13} />
                          </button>
                        )}
                        {r.estado === "En estancia" && r.saldo === 0 && (
                          <button
                            disabled={busy}
                            onClick={() => change(r, "Finalizada")}
                          >
                            Finalizar estadía
                          </button>
                        )}
                        <IconButton
                          aria-label={"Ver reserva de " + r.nombre}
                          onClick={() => open("detalle", r)}
                        >
                          <ChevronRight size={17} />
                        </IconButton>
                      </div>
                    </td>
                  </tr>
                )),
              )
            ) : (
              <Empty
                title={
                  data.reservas.length
                    ? "No hay reservas en este filtro"
                    : "Tu agenda está lista para comenzar"
                }
                text={
                  data.reservas.length
                    ? "Prueba otro filtro o una búsqueda diferente."
                    : "Crea la reserva y registra al huésped en un solo paso."
                }
                action={
                  <button
                    onClick={() =>
                      open("reserva")
                    }
                  >
                    <Plus size={16} />
                    Crear reserva
                  </button>
                }
              />
            )}
            <div className="table-footer">
              {reservas.length} reservas en esta vista{" "}
              <span>Selecciona una reserva para ver su detalle</span>
            </div>
          </>
        )}
        {view === "Huéspedes" && (
          <>
            <div className="toolbar">
              <label className="search wide">
                <Search size={16} />
                <input
                  placeholder="Buscar por nombre o DNI"
                  aria-label="Buscar huéspedes"
                  value={search}
                  onChange={(e) => setSearch(e.target.value)}
                />
              </label>
              <button
                onClick={async () => {
                  try {
                    setFound(await bridge("buscar", search.trim()));
                  } catch (e) {
                    setNotice({ error: true, text: e.message });
                  }
                }}
              >
                Buscar DNI en árbol
              </button>
            </div>
            {found !== undefined && (
              <div className="inline-result">
                {found
                  ? "Encontrado: " + found.nombre + " · " + found.dni
                  : "No hay un huésped con ese DNI exacto."}
              </div>
            )}
            {data.huespedes.length ? (
              rows(
                ["Nombre", "DNI", "Teléfono", ""],
                data.huespedes
                  .filter((h) => matches(h.nombre, h.dni))
                  .map((h) => (
                    <tr key={h.dni}>
                      <td>
                        <div className="person">
                          <span className="person-avatar">
                            {h.nombre.slice(0, 1)}
                          </span>
                          <strong>{h.nombre}</strong>
                        </div>
                      </td>
                      <td>{h.dni}</td>
                      <td>{h.telefono || "—"}</td>
                      <td>
                        <button
                          onClick={() => {
                            setView("Agenda");
                            open("reserva", { dni: h.dni });
                          }}
                        >
                          Reservar <ArrowUpRight size={13} />
                        </button>
                      </td>
                    </tr>
                  )),
              )
            ) : (
              <Empty
                title="Conoce a tu primer huésped"
                text="Cada DNI identifica a una persona, aunque comparta nombre con otra."
              />
            )}
          </>
        )}
        {view === "Habitaciones" &&
          rows(
            [
              "Habitación",
              "Tipo",
              "Capacidad",
              "Tarifa por noche",
              "Estado actual",
              "",
            ],
            data.habitaciones.map((h) => (
              <tr key={h.numero}>
                <td>
                  <span className="room-number">{h.numero}</span>
                </td>
                <td>{h.tipo}</td>
                <td>{h.capacidad} {h.capacidad === 1 ? "persona" : "personas"}</td>
                <td>
                  <strong>{money(h.tarifa)}</strong>
                </td>
                <td>
                  <Estado value={h.estado === "Disponible" ? "Disponible hoy" : h.estado} />
                  {h.proxima_reserva && <small>Reserva desde {fecha(h.proxima_reserva)}</small>}
                </td>
                <td>
                  {h.estado === "Disponible" && <button className="room-reserve" disabled={busy} onClick={() => open("reserva", {numero:h.numero})}>Reservar</button>}
                  <button
                    disabled={busy || !h.puede_mantenimiento}
                    title={!h.puede_mantenimiento ? "Tiene reservas vigentes; no se puede bloquear la habitación." : undefined}
                    onClick={() =>
                      ask(
                        h.mantenimiento
                          ? "Habilitar habitación"
                          : "Poner en mantenimiento",
                        "Una habitación con reservas vigentes no puede entrar en mantenimiento.",
                        () =>
                          operate("mantenimiento", { numero: h.numero }, false),
                      )
                    }
                  >
                    {h.mantenimiento ? "Habilitar" : "Mantenimiento"}
                  </button>
                </td>
              </tr>
            )),
          )}
        {view === "Cobros" && (
          <>
            <div className="summary-strip">
              <div>
                <span>Ingresos registrados</span>
                <strong>{money(data.resumen.ingresos)}</strong>
              </div>
              <div>
                <span>Saldo por cobrar</span>
                <strong>{money(data.resumen.pendiente)}</strong>
              </div>
              <p>
                Los pagos se conservan como registros.
                <br />
                Esta versión no procesa reembolsos.
              </p>
            </div>
            {data.pagos.length ? (
              rows(
                ["Huésped", "Reserva", "Momento", "Método", "Importe"],
                data.pagos.map((p) => (
                  <tr key={p.id}>
                    <td>
                      <strong>{p.nombre}</strong>
                    </td>
                    <td>{p.reserva.slice(0, 8)}</td>
                    <td>{new Date(p.fecha).toLocaleString("es-PE")}</td>
                    <td>{p.metodo}</td>
                    <td>
                      <strong>{money(p.monto)}</strong>
                    </td>
                  </tr>
                )),
              )
            ) : (
              <Empty
                title="Todavía no hay pagos"
                text="Registra un abono o cobra el total de una reserva confirmada."
              />
            )}
          </>
        )}
        {view === "Espera" && (
          <>
            <div className="explanation">
              <Clock3 size={19} />
              <p>
                Primero en llegar, primero en atender. Si la asignación falla,
                la solicitud conserva su lugar.
              </p>
              {data.espera.length > 0 && (
                <div className="row-actions">
                  <button onClick={() => open("atender")}>
                    Asignar habitación
                  </button>
                  <button
                    className="subtle danger"
                    onClick={() =>
                      ask(
                        "Retirar primera solicitud",
                        "Se retirará la primera solicitud de la cola, incluso si ha vencido.",
                        () => operate("retirar", {}, false),
                      )
                    }
                  >
                    Retirar primero
                  </button>
                </div>
              )}
            </div>
            {data.espera.length ? (
              rows(
                ["Turno", "Huésped", "Entrada", "Salida", "Personas"],
                data.espera.map((s) => (
                  <tr key={s.orden}>
                    <td>
                      <span className="turn">
                        {String(s.orden).padStart(2, "0")}
                      </span>
                    </td>
                    <td>
                      <strong>{s.nombre}</strong>
                      <small>{s.dni}</small>
                    </td>
                    <td>
                      {fecha(s.entrada)}
                      {s.entrada < data.hoy && (
                        <small className="balance">Solicitud vencida</small>
                      )}
                    </td>
                    <td>{fecha(s.salida)}</td>
                    <td>{s.personas}</td>
                  </tr>
                )),
              )
            ) : (
              <Empty
                title="No hay solicitudes pendientes"
                text="Añade una solicitud cuando no encuentres habitación para las fechas solicitadas."
              />
            )}
          </>
        )}
        {view === "Historial" && (
          <>
            <div className="toolbar">
              <span className="muted">
                Lista doblemente enlazada · {data.historial.length} operaciones
              </span>
              <button onClick={() => setReverse(!reverse)}>
                <ArrowLeftRight size={16} />
                {reverse ? "Más recientes primero" : "Más antiguas primero"}
              </button>
            </div>
            {data.historial.length ? (
              rows(
                ["Momento", "Operación"],
                (reverse ? data.historial : [...data.historial].reverse()).map(
                  (h, i) => (
                    <tr key={i}>
                      <td>{new Date(h.fecha).toLocaleString("es-PE")}</td>
                      <td>{h.accion}</td>
                    </tr>
                  ),
                ),
              )
            ) : (
              <Empty
                title="El historial empieza contigo"
                text="Las operaciones guardadas aparecerán aquí."
              />
            )}
          </>
        )}
        {view === "Reportes" && (
          <div className="settings">
            <section>
              <h2>Resumen por período</h2>
              <p>
                Los cobros se agrupan por fecha de pago. Las reservas y noches
                corresponden a las llegadas del período, excluyendo
                cancelaciones.
              </p>
              <form
                className="report-form"
                onSubmit={async (e) => {
                  e.preventDefault();
                  const p = Object.fromEntries(new FormData(e.currentTarget));
                  try {
                    setReport(await bridge("reportes", p.entrada, p.salida));
                  } catch (error) {
                    setNotice({ error: true, text: error.message });
                  }
                }}
              >
                <Field
                  label="Desde"
                  name="entrada"
                  type="date"
                  defaultValue={data.hoy}
                />
                <Field
                  label="Hasta"
                  name="salida"
                  type="date"
                  defaultValue={data.hoy}
                />
                <button className="primary" type="submit">
                  Consultar
                </button>
              </form>
              {report &&
                (report.ok ? (
                  <dl>
                    <div>
                      <dt>Ingresos cobrados</dt>
                      <dd>{money(report.ingresos)}</dd>
                    </div>
                    <div>
                      <dt>Pagos registrados</dt>
                      <dd>{report.pagos}</dd>
                    </div>
                    <div>
                      <dt>Reservas con llegada en el período</dt>
                      <dd>{report.reservas}</dd>
                    </div>
                    <div>
                      <dt>Noches contratadas de esas reservas</dt>
                      <dd>{report.noches}</dd>
                    </div>
                  </dl>
                ) : (
                  <div className="notice error" role="alert">
                    {report.mensaje}
                  </div>
                ))}
            </section>
            <section>
              <h2>Estado actual de habitaciones</h2>
              {rows(
                ["Estado", "Cantidad"],
                ["Disponible", "Ocupada", "Mantenimiento"].map((estado) => (
                  <tr key={estado}>
                    <td>
                      <Estado value={estado} />
                    </td>
                    <td>
                      {
                        data.habitaciones.filter((h) => h.estado === estado)
                          .length
                      }
                    </td>
                  </tr>
                )),
              )}
              <p>
                “Disponible” significa sin estancia abierta ni mantenimiento.
                Para una fecha futura, consulta la disponibilidad al crear la
                reserva.
              </p>
            </section>
          </div>
        )}
        {view === "Datos" && (
          <div className="settings">
            <section>
              <h2>Copias de seguridad</h2>
              <p>
                Python guarda los cambios en un archivo JSON fuera de la
                aplicación. Conserva también una copia del guardado anterior.
              </p>
              <div className="actions">
                <button disabled={busy} onClick={() => file("exportar")}>
                  <ArrowDownToLine size={16} />
                  Exportar JSON
                </button>
                <button
                  disabled={busy}
                  onClick={() =>
                    ask(
                      "Importar una copia",
                      "Reemplazará los datos actuales. Se validará el archivo y se conservará una copia anterior.",
                      () => file("importar"),
                    )
                  }
                >
                  <ArrowUpFromLine size={16} />
                  Importar JSON
                </button>
              </div>
            </section>
            <section>
              <h2>El motor del curso</h2>
              <p>
                Estas estructuras se implementan desde cero en Python y
                participan en las operaciones del hotel.
              </p>
              <dl>
                <div>
                  <dt>Lista simplemente enlazada + cola</dt>
                  <dd>
                    Solicitudes pendientes en orden FIFO. Encolar y desencolar:
                    O(1).
                  </dd>
                </div>
                <div>
                  <dt>Lista doblemente enlazada</dt>
                  <dd>
                    Historial y recorrido en ambos sentidos. Agregar: O(1),
                    recorrer: O(n).
                  </dd>
                </div>
                <div>
                  <dt>Árbol binario de búsqueda</dt>
                  <dd>
                    Huéspedes por DNI. Búsqueda: O(h); peor caso O(n). Sin AVL.
                  </dd>
                </div>
                <div>
                  <dt>Merge Sort y recursión</dt>
                  <dd>Agenda por fecha o importe. Estable, O(n log n).</dd>
                </div>
                <div>
                  <dt>Listas, excepciones y archivos</dt>
                  <dd>
                    Registros del hotel, validaciones y persistencia JSON.
                  </dd>
                </div>
              </dl>
            </section>
            <section>
              <h2>Ejemplo para la demostración</h2>
              <p>
                Carga dos huéspedes ficticios y dos reservas. Solo se permite si
                todavía no hay registros de huéspedes, reservas, pagos ni
                espera.
              </p>
              <button
                disabled={busy}
                onClick={() =>
                  ask(
                    "Cargar ejemplo ficticio",
                    "Las reservas se crearán con fechas a partir de hoy.",
                    () => operate("demo", {}, false),
                  )
                }
              >
                Cargar ejemplo
              </button>
            </section>
            <section>
              <h2>Alcance</h2>
              <p>
                Prototipo académico para una computadora y un operador. Sin
                facturación fiscal, reembolsos ni acceso compartido. Las
                reservas vencidas y los turnos de espera se gestionan
                manualmente. Las salidas anticipadas no recalculan el total.
              </p>
            </section>
          </div>
        )}
        <footer className="page-footer">
          <span>Sistema de Gestión de Reservas de Hotel</span>
          <span>Datos guardados en este equipo</span>
        </footer>
      </main>
      {panel && (
        <>
          <div
            className="panel-scrim"
            onClick={() => !busy && setPanel(null)}
          />
          <aside
            className="editor glass"
            ref={panelRef}
            role="dialog"
            aria-modal="true"
            onKeyDown={keepFocus}
            aria-label="Editor de recepción"
          >
            <div className="editor-head">
              <div>
                <span className="panel-label">Recepción</span>
                <h2>
                  {
                    {
                      reserva: "Nueva reserva",
                      huesped: "Registrar huésped",
                      habitacion: "Nueva habitación",
                      cobro: "Registrar pago",
                      espera: "Solicitud de espera",
                      atender: "Asignar habitación",
                      detalle: "Detalle de reserva",
                    }[panel.type]
                  }
                </h2>
              </div>
              <IconButton
                aria-label="Cerrar panel"
                disabled={busy}
                onClick={() => setPanel(null)}
              >
                <X size={20} />
              </IconButton>
            </div>
            {notice?.error && (
              <div className="panel-error" role="alert">
                {notice.text}
              </div>
            )}
            {panel.type === "detalle" ? (
              <div className="detail">
                <Estado value={panel.record.estado} />
                <h3>{panel.record.nombre}</h3>
                <p>DNI {panel.record.dni}</p>
                <dl>
                  <div>
                    <dt>Habitación</dt>
                    <dd>{panel.record.habitacion}</dd>
                  </div>
                  <div>
                    <dt>Entrada</dt>
                    <dd>{panel.record.entrada}</dd>
                  </div>
                  <div>
                    <dt>Salida</dt>
                    <dd>{panel.record.salida}</dd>
                  </div>
                  <div>
                    <dt>Personas</dt>
                    <dd>{panel.record.personas}</dd>
                  </div>
                  <div>
                    <dt>Total</dt>
                    <dd>{money(panel.record.total)}</dd>
                  </div>
                  <div>
                    <dt>Saldo</dt>
                    <dd>{panel.record.estado === "Cancelada" ? "No exigible" : money(panel.record.saldo)}</dd>
                  </div>
                </dl>
                <p className="muted">Código: {panel.record.id}</p>
                <div className="detail-actions">
                  {panel.record.estado === "Confirmada" && (
                    <>
                      <button
                        className="primary"
                        onClick={() => change(panel.record, "En estancia")}
                      >
                        Recibir huésped
                      </button>
                      <button
                        className="danger"
                        onClick={() => change(panel.record, "Cancelada")}
                      >
                        Cancelar reserva
                      </button>
                    </>
                  )}
                  {panel.record.estado === "En estancia" && (
                    <button
                      className="primary"
                      onClick={() => change(panel.record, "Finalizada")}
                    >
                      Finalizar estadía
                    </button>
                  )}
                  {panel.record.saldo > 0 &&
                    ["Confirmada", "En estancia"].includes(
                      panel.record.estado,
                    ) && (
                      <button onClick={() => open("cobro", panel.record)}>
                        Registrar pago
                      </button>
                    )}
                </div>
              </div>
            ) : (
              <form ref={formRef} onSubmit={submit} onChange={cotizar}>
                <div className="form-body">
                  {["reserva", "espera"].includes(panel.type) && (
                    <>
                      {panel.type === "reserva" ? <>
                        <input type="hidden" name="nuevo" value={knownGuest ? "0" : "1"}/>
                        <Field label="DNI del huésped" name="dni" inputMode="numeric" pattern="[0-9]{8}" maxLength="8" placeholder="8 dígitos" value={guestDni} onChange={e=>setGuestDni(e.target.value)}/>
                        <Field label={knownGuest ? "Huésped encontrado" : "Nombre completo"} name="nombre" minLength="2" maxLength="100" autoComplete="name" value={knownGuest?.nombre || guestName} readOnly={Boolean(knownGuest)} onChange={e=>setGuestName(e.target.value)}/>
                      </> : <Field label="Huésped" name="dni" defaultValue={panel.record?.dni || ""}>{peopleOptions()}</Field>}
                      {panel.type === "reserva" && (
                        <Field label="Habitación" name="numero" defaultValue={panel.record?.numero || ""}>
                          {roomOptions()}
                        </Field>
                      )}
                      <div className="two-fields">
                        <Field
                          label="Fecha de entrada"
                          name="entrada"
                          type="date"
                          min={data.hoy}
                          defaultValue={data.hoy}
                        />
                        <Field
                          label="Fecha de salida"
                          name="salida"
                          type="date"
                          min={data.hoy}
                          defaultValue={panel.type === "reserva" ? nextDay : undefined}
                        />
                      </div>
                      <Field
                        label="Cantidad de personas"
                        name="personas"
                        type="number"
                        min="1"
                        max="20"
                        defaultValue="1"
                      />

                    </>
                  )}
                  {panel.type === "huesped" && (
                    <>
                      <Field
                        label="DNI"
                        name="dni"
                        inputMode="numeric"
                        pattern="[0-9]{8}"
                        maxLength="8"
                        placeholder="8 dígitos"
                      />
                      <Field
                        label="Nombre completo"
                        name="nombre"
                        minLength="2"
                        maxLength="100"
                        autoComplete="name"
                      />
                      <Field
                        label="Teléfono (opcional)"
                        name="telefono"
                        type="tel"
                        required={false}
                        maxLength="30"
                        autoComplete="tel"
                      />
                    </>
                  )}
                  {panel.type === "habitacion" && (
                    <>
                      <Field
                        label="Número de habitación"
                        name="numero"
                        pattern="[0-9]{1,4}"
                        maxLength="4"
                      />
                      <Field label="Tipo" name="tipo">
                        {["Simple", "Doble", "Matrimonial", "Suite"].map(
                          (t) => (
                            <option key={t}>{t}</option>
                          ),
                        )}
                      </Field>
                      <Field
                        label="Capacidad"
                        name="capacidad"
                        type="number"
                        min="1"
                        max="20"
                        defaultValue="1"
                      />
                      <Field
                        label="Tarifa por noche (S/)"
                        name="tarifa"
                        type="number"
                        min="0.01"
                        max="1000000"
                        step="0.01"
                      />
                    </>
                  )}
                  {panel.type === "cobro" && (
                    <>
                      <Field
                        label="Reserva"
                        name="id"
                        defaultValue={panel.record?.id || ""}
                      >
                        <option value="">Selecciona una reserva</option>
                        {eligible.map((r) => (
                          <option key={r.id} value={r.id}>
                            {r.nombre} · {r.habitacion} · saldo {money(r.saldo)}
                          </option>
                        ))}
                      </Field>
                      <Field
                        label="Monto a cobrar (S/)"
                        name="monto"
                        type="number"
                        step="0.01"
                        min="0.01"
                        defaultValue={
                          panel.record
                            ? (panel.record.saldo / 100).toFixed(2)
                            : ""
                        }
                      />
                      <Field label="Método" name="metodo">
                        {["Efectivo", "Tarjeta", "Yape", "Transferencia"].map(
                          (t) => (
                            <option key={t}>{t}</option>
                          ),
                        )}
                      </Field>
                      <p className="form-note">
                        El pago no puede superar el saldo. Puedes registrar
                        abonos parciales.
                      </p>
                    </>
                  )}
                  {panel.type === "atender" && (
                    <>
                      <p className="form-note">
                        Primera solicitud:{" "}
                        <strong>{data.espera[0]?.nombre}</strong>
                      </p>
                      <Field label="Habitación para asignar" name="numero">
                        {roomOptions()}
                      </Field>
                    </>
                  )}
                </div>
                {panel.type === "reserva" && <div className="compact-quote"><div><span>Total de la estadía</span><small>{quote?.ok ? `${quote.noches} ${quote.noches === 1 ? "noche" : "noches"} · ${quote.disponible ? "Disponible" : "No disponible"}` : quote?.mensaje || "Completa habitación y fechas"}</small></div><strong>{quote?.ok ? money(quote.total) : "—"}</strong></div>}
                <div className="editor-footer">
                  <button
                    type="button"
                    disabled={busy}
                    onClick={() => setPanel(null)}
                  >
                    Volver
                  </button>
                  <button
                    className="primary clay"
                    type="submit"
                    disabled={busy || (panel.type === "reserva" && (!quote?.ok || !quote.disponible))}
                  >
                    {busy
                      ? "Guardando…"
                      : panel.type === "reserva"
                        ? "Confirmar reserva"
                        : panel.type === "cobro"
                          ? "Guardar pago"
                          : panel.type === "atender"
                            ? "Atender solicitud"
                            : "Guardar"}
                  </button>
                </div>
              </form>
            )}
          </aside>
        </>
      )}
      <dialog
        ref={dialogRef}
        className="confirmation"
        onCancel={(e) => {
          if (busy) e.preventDefault();
          else setConfirm(null);
        }}
      >
        {confirm && (
          <>
            <h2>{confirm.title}</h2>
            <p>{confirm.text}</p>
            <div className="actions">
              <button disabled={busy} onClick={() => setConfirm(null)}>
                Volver
              </button>
              <button
                className="primary"
                disabled={busy}
                onClick={async () => {
                  await confirm.run();
                  setConfirm(null);
                }}
              >
                {busy ? "Procesando…" : "Confirmar"}
              </button>
            </div>
          </>
        )}
      </dialog>
    </div>
  );
}
createRoot(document.getElementById("root")).render(<App />);

