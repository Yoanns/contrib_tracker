import streamlit as st
from models import Tracker
import storage
import matplotlib.pyplot as plt

st.set_page_config(page_title="Sibling Contributions Tracker", page_icon=":moneybag:", layout="centered")

@st.cache_resource
def _load_tracker_once() -> Tracker:
    """
    Load tracker once per session and keep in memory.
    We still explicitly save to CSV on changes for persistence.
    """
    return storage.load_tracker()

def save_all(t: Tracker) -> None:
    """
    Persist current tracker state to CSV files.
    """
    storage.save_members(t.all_members())
    storage.save_contributions(t.history())

def page_members(t: Tracker) -> None:
    """
    Members page: list and add members.
    """
    st.header("Members")
    st.caption(f"Data folder: {storage.data_dir()}")
    with st.form("add_member"):
        name = st.text_input("Member name")
        monthly = st.number_input("Monthly amount (optional)", min_value=0.0, value=0.0, step=1.0)
        submitted = st.form_submit_button("Add member")
        if submitted:
            if t.add_member(name, monthly):
                save_all(t)
                st.success(f"Added member: {name}")
            else:
                st.warning("Member exists or invalid name.")

    # Display members
    members = [{"name": m.name, "monthly_amount": m.monthly_amount} for m in t.all_members()]
    st.subheader("Current members")
    if members:
        st.dataframe(members, width='stretch')
    else:
        st.info("No members yet.")

def page_contributions(t: Tracker) -> None:
    """
    Contributions page: record and view contributions.
    """
    st.header("Contributions")
    mem_names = [m.name for m in t.all_members()]
    if not mem_names:
        st.info("Add members first on the Members page.")
        return

    with st.form("add_contribution"):
        member = st.selectbox("Member", mem_names)
        amount = st.number_input("Amount", min_value=0.01, value=10.0, step=1.0)
        date_iso = st.date_input("Date").isoformat()
        submitted = st.form_submit_button("Record contribution")
        if submitted:
            if t.record_contribution(member, amount, when=date_iso):
                save_all(t)
                st.success(f"Recorded {amount:.2f} for {member} on {date_iso}")
            else:
                st.warning("Failed to record contribution (check member and amount).")

    # View contributions
    st.subheader("All contributions")
    rows = [{"member": c.member, "date": c.date, "amount": c.amount} for c in t.history()]
    if rows:
        st.dataframe(rows, width='stretch')
    else:
        st.info("No contributions yet.")

def render_totals_bar(t: Tracker) -> None:
    """
    Render a Matplotlib bar chart of totals by member.
    """
    totals = t.totals_by_member()
    if not totals:
        st.info("No data to chart yet.")
        return

    names = list(totals.keys())
    values = [totals[n] for n in names]

    fig, ax = plt.subplots(figsize=(6, 3))
    ax.bar(names, values, color="#4C78A8")
    ax.set_title("Total Contributions by Member")
    ax.set_ylabel("Amount")
    ax.set_xlabel("Member")
    ax.grid(axis="y", linestyle="--", alpha=0.5)
    plt.xticks(rotation=15)
    st.pyplot(fig)

def page_reports(t: Tracker) -> None:
    """
    Reports page: show per-member totals and charts.
    """
    st.header("Reports")
    totals = t.totals_by_member()
    st.subheader("Totals by member")
    if totals:
        table = [{"member": k, "total": v} for k, v in totals.items()]
        st.dataframe(table, width='stretch')
        st.subheader("Visualization")
        render_totals_bar(t)
    else:
        st.info("No totals to show yet.")

def main() -> None:
    """
    App entry point.
    """
    st.title(":moneybag: Sibling Contributions Tracker")
    t = _load_tracker_once()

    # page = st.sidebar.radio("Navigate", ["Members", "Contributions", "Reports"])
    # if page == "Members":
    #     page_members(t)
    # elif page == "Contributions":
    #     page_contributions(t)
    # else:
    #     page_reports(t)

    tab1, tab2, tab3 = st.tabs(["Members", "Contributions", "Reports"])
    with tab1:
        page_members(t)
    with tab2:
        page_contributions(t)
    with tab3:
        page_reports(t)

if __name__ == "__main__":
    main()
