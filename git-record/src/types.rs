    pub file_states: Vec<(PathBuf, FileState)>,
pub type FileMode = usize;

pub struct FileState {
    /// The Unix file mode of the file, if available.
    ///
    /// This value is not directly modified by the UI; instead, construct a
    /// [`Section::FileMode`] and use the [`FileState::get_file_mode`] function
    /// to read a user-provided updated to the file mode function to read a
    /// user-provided updated to the file mode
    pub file_mode: Option<FileMode>,
    /// The set of [`Section`]s inside the file.
    pub sections: Vec<Section>,
}
impl FileState {
    /// An absent file.
    pub fn absent() -> Self {
        unimplemented!("FileState::absent")
    }
    /// A binary file.
    pub fn binary() -> Self {
        unimplemented!("FileState::binary")
    }
    pub fn count_changed_sections(&self) -> usize {
        let Self {
            file_mode: _,
            sections,
        } = self;
        sections
            .iter()
            .filter(|section| match section {
                Section::Unchanged { .. } => false,
                Section::Changed { .. } => true,
                Section::FileMode { .. } => {
                    unimplemented!("count_changed_sections for Section::FileMode")
                }
            })
            .count()
    }

    /// Get the new Unix file mode. If the user selected a
    /// [`Section::FileMode`], then returns that file mode. Otherwise, returns
    /// the `file_mode` value that this [`FileState`] was constructed with.
    pub fn get_file_mode(&self) -> Option<FileMode> {
        let Self {
            file_mode,
            sections,
        } = self;
        sections
            .iter()
            .find_map(|section| match section {
                Section::Unchanged { .. }
                | Section::Changed { .. }
                | Section::FileMode {
                    is_selected: false,
                    before: _,
                    after: _,
                } => None,

                Section::FileMode {
                    is_selected: true,
                    before: _,
                    after,
                } => Some(*after),
            })
            .or(*file_mode)
        let Self {
            file_mode: _,
            sections,
        } = self;
        for section in sections {
            match section {
                Section::Unchanged { contents } => {
                    for line in contents {
                        acc_selected.push_str(line);
                        acc_unselected.push_str(line);
                    }
                }
                Section::Changed { before, after } => {
                    for SectionChangedLine { is_selected, line } in before {
                        // Note the inverted condition here.
                        if !*is_selected {
                            acc_selected.push_str(line);
                        } else {
                            acc_unselected.push_str(line);
                    }

                    for SectionChangedLine { is_selected, line } in after {
                        if *is_selected {
                            acc_selected.push_str(line);
                        } else {
                            acc_unselected.push_str(line);
                Section::FileMode {
                    is_selected: _,
                    before: _,
                    after: _,
                } => {
                    unimplemented!("get_selected_contents for Section::FileMode");
                }
pub enum Section {
        before: Vec<SectionChangedLine>,
        after: Vec<SectionChangedLine>,
    },

    /// The Unix file mode of the file changed, and the user needs to select
    /// whether to accept that mode change or not.
    FileMode {
        /// Whether or not the file mode change was accepted.
        is_selected: bool,

        /// The old file mode.
        before: FileMode,

        /// The new file mode.
        after: FileMode,
/// A changed line inside a `Section`.
pub struct SectionChangedLine {