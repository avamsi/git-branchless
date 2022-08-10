use std::{borrow::Cow, path::PathBuf};
pub struct RecordState<'a> {
    pub file_states: Vec<(PathBuf, FileState<'a>)>,
pub struct FileState<'a> {
    pub sections: Vec<Section<'a>>,
impl FileState<'_> {
pub enum Section<'a> {
        contents: Vec<Cow<'a, str>>,
        before: Vec<SectionChangedLine<'a>>,
        after: Vec<SectionChangedLine<'a>>,
pub struct SectionChangedLine<'a> {
    pub line: Cow<'a, str>,
}

impl<'a> SectionChangedLine<'a> {
    /// Make a copy of this [`SectionChangedLine`] that borrows the content of
    /// the line from the original.
    pub fn borrow_line(&'a self) -> Self {
        let Self { is_selected, line } = self;
        Self {
            is_selected: *is_selected,
            line: Cow::Borrowed(line),
        }
    }