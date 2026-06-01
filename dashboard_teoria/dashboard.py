from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCENARIOS = ("SMALL_TEST", "MIDDLE_TEST", "BIG_TEST")
RESULT_PATTERN = re.compile(
    r"len\s+set\s+(?P<n>\d+)\s+time:\s+(?P<time>[+-]?(?:\d+(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)"
)


@dataclass(frozen=True)
class ResultFile:
    language: str
    scenario: str
    path: Path


def expected_result_files() -> list[ResultFile]:
    files: list[ResultFile] = []

    for scenario in SCENARIOS:
        files.append(
            ResultFile(
                language="C",
                scenario=scenario,
                path=PROJECT_ROOT / "c" / "case_tests_c" / scenario,
            )
        )
        files.append(
            ResultFile(
                language="Go",
                scenario=scenario,
                path=PROJECT_ROOT / "go" / "case_tests_go" / scenario,
            )
        )

    return files


def parse_result_line(line: str) -> tuple[int, float] | None:
    match = RESULT_PATTERN.search(line)
    if not match:
        return None

    return int(match.group("n")), float(match.group("time"))


def read_result_file(result_file: ResultFile) -> tuple[list[dict[str, object]], int]:
    rows: list[dict[str, object]] = []
    ignored_lines = 0

    with result_file.path.open("r", encoding="utf-8") as file:
        for line in file:
            parsed = parse_result_line(line)
            if parsed is None:
                if line.strip():
                    ignored_lines += 1
                continue

            n, execution_time = parsed
            rows.append(
                {
                    "linguagem": result_file.language,
                    "cenario": result_file.scenario,
                    "n": n,
                    "tempo_execucao": execution_time,
                    "arquivo": str(result_file.path.relative_to(PROJECT_ROOT)),
                }
            )

    return rows, ignored_lines


@st.cache_data(show_spinner=False)
def load_results() -> tuple[pd.DataFrame, list[str], list[str]]:
    rows: list[dict[str, object]] = []
    missing_files: list[str] = []
    parse_warnings: list[str] = []

    for result_file in expected_result_files():
        relative_path = str(result_file.path.relative_to(PROJECT_ROOT))

        if not result_file.path.exists():
            missing_files.append(relative_path)
            continue

        file_rows, ignored_lines = read_result_file(result_file)
        rows.extend(file_rows)

        if ignored_lines:
            parse_warnings.append(
                f"{relative_path}: {ignored_lines} linha(s) não correspondem ao formato esperado."
            )

    return pd.DataFrame(rows), missing_files, parse_warnings


def build_summary(results: pd.DataFrame) -> pd.DataFrame:
    summary = (
        results.groupby(["linguagem", "cenario", "n"], as_index=False)
        .agg(
            quantidade_execucoes=("tempo_execucao", "count"),
            media_tempo=("tempo_execucao", "mean"),
            desvio_padrao=("tempo_execucao", "std"),
            tempo_minimo=("tempo_execucao", "min"),
            tempo_maximo=("tempo_execucao", "max"),
        )
        .sort_values(["n", "linguagem", "cenario"])
    )

    summary["desvio_padrao"] = summary["desvio_padrao"].fillna(0.0)
    return summary


def show_file_warnings(missing_files: list[str], parse_warnings: list[str]) -> None:
    if missing_files:
        st.warning(
            "Alguns arquivos de resultado ainda não existem. O dashboard continuará com os dados disponíveis:\n\n"
            + "\n".join(f"- `{path}`" for path in missing_files)
        )

    for warning in parse_warnings:
        st.warning(warning)


def show_execution_count_warning(summary: pd.DataFrame) -> None:
    under_sampled = summary[summary["quantidade_execucoes"] < 30]
    if under_sampled.empty:
        return

    st.info(
        "Há grupos com menos de 30 execuções. A especificação da disciplina recomenda 30 rodadas "
        "por tamanho de entrada; os gráficos e tabelas abaixo usam os dados disponíveis."
    )


def format_summary(summary: pd.DataFrame) -> pd.DataFrame:
    return summary.rename(
        columns={
            "linguagem": "Linguagem",
            "cenario": "Cenário",
            "n": "n",
            "quantidade_execucoes": "Quantidade de execuções",
            "media_tempo": "Média do tempo",
            "desvio_padrao": "Desvio-padrão",
            "tempo_minimo": "Tempo mínimo",
            "tempo_maximo": "Tempo máximo",
        }
    )


def render_summary_table(summary: pd.DataFrame) -> None:
    st.subheader("Tabela consolidada")
    st.dataframe(
        format_summary(summary),
        use_container_width=True,
        hide_index=True,
        column_config={
            "Média do tempo": st.column_config.NumberColumn(format="%.9f"),
            "Desvio-padrão": st.column_config.NumberColumn(format="%.9f"),
            "Tempo mínimo": st.column_config.NumberColumn(format="%.9f"),
            "Tempo máximo": st.column_config.NumberColumn(format="%.9f"),
        },
    )

    csv = summary.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Baixar tabela consolidada em CSV",
        data=csv,
        file_name="tabela_consolidada_resultados.csv",
        mime="text/csv",
    )


def render_average_time_chart(summary: pd.DataFrame, use_log_scale: bool) -> None:
    st.subheader("Tempo médio por tamanho de entrada")
    plot_data = summary.sort_values(["linguagem", "n", "cenario"])

    fig = px.line(
        plot_data,
        x="n",
        y="media_tempo",
        color="linguagem",
        markers=True,
        hover_data=["cenario", "quantidade_execucoes"],
        labels={
            "n": "Tamanho da entrada (n)",
            "media_tempo": "Tempo médio de execução",
            "linguagem": "Linguagem",
            "cenario": "Cenário",
            "quantidade_execucoes": "Quantidade de execuções",
        },
    )
    fig.update_layout(legend_title_text="Linguagem")
    if use_log_scale:
        fig.update_yaxes(type="log")
    st.plotly_chart(fig, use_container_width=True)


def build_theoretical_curve(summary: pd.DataFrame) -> pd.DataFrame:
    by_n = summary.groupby("n", as_index=False)["media_tempo"].mean().sort_values("n")
    if by_n.empty:
        return by_n

    by_n["o_2_n_bruto"] = 2.0 ** by_n["n"]
    max_theoretical = by_n["o_2_n_bruto"].max()
    max_observed = by_n["media_tempo"].max()
    scale = max_observed / max_theoretical if max_theoretical and max_observed else 1.0
    by_n["O(2^n) escalada"] = by_n["o_2_n_bruto"] * scale
    return by_n


def render_theoretical_chart(summary: pd.DataFrame, use_log_scale: bool) -> None:
    st.subheader("Aderência à curva teórica O(2^n)")
    theoretical = build_theoretical_curve(summary)

    fig = go.Figure()
    for language, group in summary.groupby("linguagem"):
        ordered_group = group.sort_values("n")
        fig.add_trace(
            go.Scatter(
                x=ordered_group["n"],
                y=ordered_group["media_tempo"],
                mode="lines+markers",
                name=language,
                customdata=ordered_group[["cenario", "quantidade_execucoes"]],
                hovertemplate=(
                    "Linguagem: "
                    + language
                    + "<br>n: %{x}"
                    + "<br>Tempo médio: %{y}"
                    + "<br>Cenário: %{customdata[0]}"
                    + "<br>Execuções: %{customdata[1]}"
                    + "<extra></extra>"
                ),
            )
        )

    fig.add_trace(
        go.Scatter(
            x=theoretical["n"],
            y=theoretical["O(2^n) escalada"],
            mode="lines+markers",
            name="O(2^n) escalada",
            line={"dash": "dash", "color": "black"},
        )
    )

    fig.update_layout(
        xaxis_title="Tamanho da entrada (n)",
        yaxis_title="Tempo médio de execução",
        legend_title_text="Série",
    )
    if use_log_scale:
        fig.update_yaxes(type="log")
    st.plotly_chart(fig, use_container_width=True)


def render_boxplot(results: pd.DataFrame) -> None:
    st.subheader("Distribuição das 30 execuções por cenário")
    plot_data = results.copy()
    plot_data["n"] = plot_data["n"].astype(str)

    fig = px.box(
        plot_data,
        x="n",
        y="tempo_execucao",
        color="linguagem",
        facet_col="cenario",
        points="all",
        labels={
            "n": "Tamanho da entrada (n)",
            "tempo_execucao": "Tempo de execução",
            "linguagem": "Linguagem",
            "cenario": "Cenário",
        },
    )
    fig.update_layout(boxmode="group")
    fig.update_yaxes(matches=None)
    st.plotly_chart(fig, use_container_width=True)


def main() -> None:
    st.set_page_config(page_title="Dashboard - Conjunto das Partes", layout="wide")
    st.title("Resultados experimentais do conjunto das partes")
    st.caption("Leitura automática dos resultados de C e Go, sem modificar os arquivos originais.")

    results, missing_files, parse_warnings = load_results()
    show_file_warnings(missing_files, parse_warnings)

    if results.empty:
        st.error(
            "Nenhum resultado válido foi encontrado. Gere os arquivos de resultado em C ou Go e recarregue esta página."
        )
        return

    scenario_filter = st.multiselect(
        "Cenários",
        options=list(SCENARIOS),
        default=list(SCENARIOS),
    )
    language_filter = st.multiselect(
        "Linguagens",
        options=sorted(results["linguagem"].unique()),
        default=sorted(results["linguagem"].unique()),
    )
    use_log_scale = st.checkbox("Usar escala logarítmica no eixo Y")

    filtered_results = results[
        results["cenario"].isin(scenario_filter) & results["linguagem"].isin(language_filter)
    ]

    if filtered_results.empty:
        st.warning("Nenhum dado corresponde aos filtros selecionados.")
        return

    summary = build_summary(filtered_results)
    show_execution_count_warning(summary)

    render_summary_table(summary)
    render_average_time_chart(summary, use_log_scale)
    render_theoretical_chart(summary, use_log_scale)
    render_boxplot(filtered_results)


if __name__ == "__main__":
    main()
